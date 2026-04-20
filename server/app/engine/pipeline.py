import asyncio
import json
import traceback
import uuid
from collections import deque
from collections.abc import Mapping

import httpx

from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.engine.cleaner import clean_content
from app.engine.downloader import fetch_dynamic, fetch_static
from app.engine.parser import (
    detail_request_delay_seconds,
    detail_retry_count,
    detail_retry_policy,
    detail_retry_sleep_seconds,
    detail_rules_json,
    detail_url_limit,
    extract_list_follow_urls,
    extract_next_list_page_url,
    anti_bot_block_backoff_seconds,
    anti_bot_block_status_codes,
    anti_bot_retry_on_block,
    looks_like_anti_bot_challenge,
    fetch_cookie_domain_override,
    fetch_http_cookies,
    fetch_http_headers,
    fetch_login_flow,
    fetch_proxy_config,
    fetch_timeout_seconds,
    list_page_fetch_budget,
    list_request_delay_seconds,
    parse_with_readability,
    parse_with_rules,
    resolve_list_page_urls,
    should_retry_detail_failure,
)
from app.engine.validator import quality_score
from app.repositories.data_repo import DataRepository
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.utils.file import save_snapshot
from app.utils.hash import sha256_text


class AntiBotBlockedError(RuntimeError):
    """Raised when the fetched page appears to be blocked by anti-bot controls."""


def _summary_payload_json(
    *,
    run_id: str,
    mode: str,
    metrics: Mapping[str, object],
) -> str:
    payload = {
        "kind": "run_summary",
        "run_id": run_id,
        "mode": mode,
        "metrics": dict(metrics),
    }
    return json.dumps(payload, ensure_ascii=False)


async def _collect_and_store_one(
    *,
    task_id: int,
    run_id: str,
    page_url: str,
    parser_rules: str | None,
    log_repo: LogRepository,
    data_repo: DataRepository,
    crawl_rules: dict[str, object] | None = None,
) -> str:
    """Download one URL, parse, persist. Returns ``stored`` or ``skipped_hash``."""
    html = await _download_page(
        url=page_url,
        log_repo=log_repo,
        task_id=task_id,
        run_id=run_id,
        crawl_rules=crawl_rules,
    )
    parsed = await _parse_page(
        html,
        parser_rules=parser_rules,
        source_url=page_url,
        log_repo=log_repo,
        task_id=task_id,
        run_id=run_id,
    )
    cleaned = clean_content(parsed["content_html"])
    score = quality_score(parsed.get("title"), cleaned["content_text"])

    if score < 40:
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=(
                f"[run={run_id}] Task {task_id} produced low quality content: {score} ({page_url})"
            ),
        )

    content_hash = sha256_text(cleaned["content_text"])
    duplicate = await data_repo.get_by_hash(content_hash)
    if duplicate is not None:
        await log_repo.create(
            level="INFO",
            task_id=task_id,
            message=(
                f"[run={run_id}] Duplicate content detected for task {task_id}, "
                f"skipping storage ({page_url})"
            ),
        )
        return "skipped_hash"

    existing = await data_repo.get_by_source_url(page_url)
    if existing is not None:
        stored = await data_repo.update(
            existing,
            task_id=task_id,
            title=parsed.get("title"),
            content_html=cleaned["content_html"],
            content_text=cleaned["content_text"],
            quality_score=score,
            content_hash=content_hash,
        )
    else:
        stored = await data_repo.create(
            task_id=task_id,
            title=parsed.get("title"),
            content_html=cleaned["content_html"],
            content_text=cleaned["content_text"],
            source_url=page_url,
            snapshot_path=None,
            quality_score=score,
            content_hash=content_hash,
        )

    try:
        snapshot_path = save_snapshot(data_id=stored.id, html=html)
        await data_repo.update_snapshot_path(data=stored, snapshot_path=snapshot_path)
    except Exception as exc:
        await log_repo.create(
            level="ERROR",
            task_id=task_id,
            message=f"[run={run_id}] Snapshot save failed for data {stored.id}",
            error_stack=str(exc),
        )

    await log_repo.create(
        level="INFO",
        task_id=task_id,
        message=f"[run={run_id}] Task {task_id} collected data item {stored.id} ({page_url})",
    )
    return "stored"


async def _collect_and_store_one_retrying(
    *,
    task_id: int,
    run_id: str,
    page_url: str,
    parser_rules: str | None,
    log_repo: LogRepository,
    data_repo: DataRepository,
    crawl_rules: dict[str, object] | None,
) -> str:
    """Like ``_collect_and_store_one`` with optional retries and same return values."""
    extra = detail_retry_count(crawl_rules)
    total = extra + 1
    policy = detail_retry_policy(crawl_rules)
    last_exc: Exception | None = None
    for attempt in range(total):
        try:
            return await _collect_and_store_one(
                task_id=task_id,
                run_id=run_id,
                page_url=page_url,
                parser_rules=parser_rules,
                log_repo=log_repo,
                data_repo=data_repo,
                crawl_rules=crawl_rules,
            )
        except Exception as exc:
            last_exc = exc
            if attempt + 1 >= total:
                break
            retryable = isinstance(exc, AntiBotBlockedError) or should_retry_detail_failure(
                exc, policy
            )
            if not retryable:
                await log_repo.create(
                    level="INFO",
                    task_id=task_id,
                    message=(
                        f"[run={run_id}] detail failure not retried (policy={policy}) "
                        f"{page_url}: {exc!s}"
                    ),
                )
                break
            wait_sec = detail_retry_sleep_seconds(crawl_rules, attempt)
            await log_repo.create(
                level="WARNING",
                task_id=task_id,
                message=(
                    f"[run={run_id}] detail page failed ({page_url}), "
                    f"sleep {wait_sec:.1f}s then retry "
                    f"{attempt + 2}/{total}: {exc!s}"
                ),
            )
            await asyncio.sleep(wait_sec)
    assert last_exc is not None
    raise last_exc


async def run_task(task_id: int) -> None:
    async with AsyncSessionLocal() as session:
        task_repo = TaskRepository(session)
        data_repo = DataRepository(session)
        log_repo = LogRepository(session)

        task = await task_repo.get_by_id(task_id)
        if task is None:
            await log_repo.create(
                level="ERROR",
                task_id=task_id,
                message=f"Task {task_id} not found",
            )
            raise ValueError(f"Task {task_id} not found")

        run_id = uuid.uuid4().hex[:12]
        await log_repo.create(
            level="INFO",
            task_id=task_id,
            message=f"[run={run_id}] Task {task_id} pipeline started",
        )

        try:
            rules_loaded = _load_rules(task.parser_rules)
            crawl_mode = None
            if isinstance(rules_loaded, dict):
                raw_mode = rules_loaded.get("crawl_mode")
                if isinstance(raw_mode, str):
                    crawl_mode = raw_mode.strip().lower()

            if crawl_mode == "list_follow":
                list_budget = list_page_fetch_budget(rules_loaded)
                queue: deque[str] = deque(
                    resolve_list_page_urls(task.start_url, rules_loaded)
                )
                scheduled_list: set[str] = set(queue)
                delay_sec = list_request_delay_seconds(rules_loaded)
                detail_rules = detail_rules_json(rules_loaded)
                detail_sleep = detail_request_delay_seconds(rules_loaded)
                await log_repo.create(
                    level="INFO",
                    task_id=task_id,
                    message=(
                        f"[run={run_id}] list_follow: list fetch budget={list_budget}, "
                        f"initial queue={len(queue)}"
                    ),
                )
                detail_limit = detail_url_limit(rules_loaded)
                seen_detail: set[str] = set()
                detail_processed_count = 0
                detail_success_count = 0
                detail_skipped_count = 0
                detail_failed_count = 0
                last_error: Exception | None = None
                any_item_completed = False
                list_fetches = 0
                while queue and list_fetches < list_budget:
                    remaining = detail_limit - detail_processed_count
                    if remaining <= 0:
                        break
                    list_url = queue.popleft()
                    list_fetches += 1
                    list_html = await _download_page(
                        url=list_url,
                        log_repo=log_repo,
                        task_id=task_id,
                        run_id=run_id,
                        crawl_rules=rules_loaded,
                    )
                    batch = extract_list_follow_urls(
                        list_html,
                        list_url,
                        rules_loaded,
                        url_cap=remaining,
                    )
                    unique_batch: list[str] = []
                    for u in batch:
                        if u in seen_detail:
                            continue
                        seen_detail.add(u)
                        unique_batch.append(u)

                    for batch_index, page_url in enumerate(unique_batch):
                        if detail_processed_count >= detail_limit:
                            break
                        detail_processed_count += 1
                        try:
                            outcome = await _collect_and_store_one_retrying(
                                task_id=task_id,
                                run_id=run_id,
                                page_url=page_url,
                                parser_rules=detail_rules,
                                log_repo=log_repo,
                                data_repo=data_repo,
                                crawl_rules=rules_loaded,
                            )
                            if outcome == "stored":
                                detail_success_count += 1
                            elif outcome == "skipped_hash":
                                detail_skipped_count += 1
                            any_item_completed = True
                        except Exception as exc:
                            detail_failed_count += 1
                            last_error = exc
                            await log_repo.create(
                                level="ERROR",
                                task_id=task_id,
                                message=(
                                    f"[run={run_id}] list_follow failed on item "
                                    f"{detail_processed_count}/{detail_limit} {page_url}"
                                ),
                                error_stack=str(exc),
                            )

                        if (
                            detail_sleep > 0
                            and detail_processed_count < detail_limit
                            and (
                                batch_index < len(unique_batch) - 1
                                or bool(queue)
                            )
                        ):
                            await asyncio.sleep(detail_sleep)

                    raw_next = rules_loaded.get("list_next_page")
                    if isinstance(raw_next, str) and raw_next.strip():
                        nxt = extract_next_list_page_url(
                            list_html, list_url, rules_loaded
                        )
                        if nxt is not None and nxt not in scheduled_list:
                            scheduled_list.add(nxt)
                            queue.append(nxt)

                    if (
                        delay_sec > 0
                        and queue
                        and list_fetches < list_budget
                        and (detail_limit - detail_processed_count) > 0
                    ):
                        await asyncio.sleep(delay_sec)
                if not seen_detail:
                    await log_repo.create(
                        level="WARNING",
                        task_id=task_id,
                        message=(
                            f"[run={run_id}] list_follow: no detail URLs from list page(s) "
                            f"(check list_item / detail_link selectors)"
                        ),
                    )
                    raise ValueError("list_follow produced zero detail URLs")

                detail_limit_hit = detail_processed_count >= detail_limit
                summary_metrics = {
                    "list_pages": list_fetches,
                    "detail_discovered": len(seen_detail),
                    "detail_processed": detail_processed_count,
                    "stored": detail_success_count,
                    "skipped_hash": detail_skipped_count,
                    "failed": detail_failed_count,
                    "detail_limit": detail_limit,
                    "detail_limit_hit": detail_limit_hit,
                    "remaining_list_queue": len(queue),
                }
                await log_repo.create(
                    level="INFO",
                    task_id=task_id,
                    message=(
                        f"[run={run_id}] 列表跟进运行摘要："
                        f"扫描列表页 {list_fetches}，发现详情 {len(seen_detail)}，"
                        f"处理 {detail_processed_count}，入库 {detail_success_count}，"
                        f"重复跳过 {detail_skipped_count}，失败 {detail_failed_count}。"
                    ),
                    run_summary=_summary_payload_json(
                        run_id=run_id,
                        mode="list_follow",
                        metrics=summary_metrics,
                    ),
                )

                if not any_item_completed and last_error is not None:
                    raise last_error
            else:
                single_outcome = await _collect_and_store_one_retrying(
                    task_id=task_id,
                    run_id=run_id,
                    page_url=task.start_url,
                    parser_rules=task.parser_rules,
                    log_repo=log_repo,
                    data_repo=data_repo,
                    crawl_rules=rules_loaded
                    if isinstance(rules_loaded, dict)
                    else None,
                )
                single_stored = 1 if single_outcome == "stored" else 0
                single_skipped = 1 if single_outcome == "skipped_hash" else 0
                single_metrics = {
                    "processed": 1,
                    "stored": single_stored,
                    "skipped_hash": single_skipped,
                    "failed": 0,
                }
                await log_repo.create(
                    level="INFO",
                    task_id=task_id,
                    message=(
                        f"[run={run_id}] 单页运行摘要：处理 1，入库 {single_stored}，"
                        f"重复跳过 {single_skipped}，失败 0。"
                    ),
                    run_summary=_summary_payload_json(
                        run_id=run_id,
                        mode="single_page",
                        metrics=single_metrics,
                    ),
                )
        except Exception:
            await log_repo.create(
                level="ERROR",
                task_id=task_id,
                message=f"[run={run_id}] Task {task_id} pipeline execution failed",
                error_stack=traceback.format_exc(),
            )
            raise


async def _download_page(
    *,
    run_id: str,
    task_id: int,
    log_repo: LogRepository,
    url: str,
    crawl_rules: dict[str, object] | None = None,
) -> str:
    default_timeout = float(get_settings().timeout)
    timeout_sec = fetch_timeout_seconds(crawl_rules, default_timeout)
    extra_headers = fetch_http_headers(crawl_rules)
    jar = fetch_http_cookies(crawl_rules)
    cookie_domain = fetch_cookie_domain_override(crawl_rules)
    login_flow = fetch_login_flow(crawl_rules)
    proxy_config = fetch_proxy_config(crawl_rules)
    if isinstance(login_flow, dict):
        session_key = login_flow.get("session_key")
        if not isinstance(session_key, str) or not session_key.strip():
            login_flow["session_key"] = f"task:{task_id}"
    block_status_codes = anti_bot_block_status_codes(crawl_rules)
    block_backoff_sec = anti_bot_block_backoff_seconds(crawl_rules)
    retry_on_block = anti_bot_retry_on_block(crawl_rules)

    static_exc: Exception | None = None
    try:
        static_html = await fetch_static(
            url,
            timeout=timeout_sec,
            headers=extra_headers,
            cookies=jar,
        )
        if not looks_like_anti_bot_challenge(static_html, crawl_rules):
            return static_html
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=(
                f"[run={run_id}] Static fetch returned suspected anti-bot challenge for "
                f"{url}, falling back to dynamic fetch"
            ),
        )
    except Exception as exc:
        static_exc = exc
        message = f"[run={run_id}] Static fetch failed for {url}, falling back to dynamic fetch"
        if isinstance(exc, httpx.HTTPStatusError):
            status_code = exc.response.status_code if exc.response is not None else 0
            if status_code in block_status_codes:
                message = (
                    f"[run={run_id}] Static fetch hit anti-bot status {status_code} for {url}, "
                    "falling back to dynamic fetch"
                )
                if block_backoff_sec > 0:
                    await asyncio.sleep(block_backoff_sec)
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=message,
            error_stack=str(exc),
        )

    proxy_on_block_only = True
    proxy_failover_enabled = True
    if isinstance(proxy_config, dict):
        proxy_on_block_only = bool(proxy_config.get("on_block_only", True))
        proxy_failover_enabled = bool(proxy_config.get("failover_enabled", True))

    primary_proxy = proxy_config if (proxy_config and not proxy_on_block_only) else None

    try:
        dynamic_html = await fetch_dynamic(
            url,
            timeout=timeout_sec,
            headers=extra_headers,
            cookies=jar,
            cookie_domain=cookie_domain,
            login_flow=login_flow,
            proxy=primary_proxy,
        )
    except Exception as dynamic_exc:
        if proxy_config and proxy_on_block_only and proxy_failover_enabled:
            await log_repo.create(
                level="WARNING",
                task_id=task_id,
                message=(
                    f"[run={run_id}] Dynamic fetch failed for {url}, retrying with proxy"
                ),
                error_stack=str(dynamic_exc),
            )
            dynamic_html = await fetch_dynamic(
                url,
                timeout=timeout_sec,
                headers=extra_headers,
                cookies=jar,
                cookie_domain=cookie_domain,
                login_flow=login_flow,
                proxy=proxy_config,
            )
        else:
            raise

    if looks_like_anti_bot_challenge(dynamic_html, crawl_rules):
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=(
                f"[run={run_id}] Dynamic fetch still looks like anti-bot challenge for {url}"
            ),
            error_stack=str(static_exc) if static_exc is not None else None,
        )
        if proxy_config and proxy_on_block_only and proxy_failover_enabled:
            await log_repo.create(
                level="WARNING",
                task_id=task_id,
                message=(
                    f"[run={run_id}] Challenge detected for {url}, retrying dynamic fetch with proxy"
                ),
            )
            proxied_html = await fetch_dynamic(
                url,
                timeout=timeout_sec,
                headers=extra_headers,
                cookies=jar,
                cookie_domain=cookie_domain,
                login_flow=login_flow,
                proxy=proxy_config,
            )
            if not looks_like_anti_bot_challenge(proxied_html, crawl_rules):
                return proxied_html
            dynamic_html = proxied_html
        if retry_on_block:
            raise AntiBotBlockedError(f"anti-bot challenge detected for {url}")
    return dynamic_html


async def _parse_page(
    html: str,
    *,
    parser_rules: str | None,
    source_url: str,
    log_repo: LogRepository,
    task_id: int,
    run_id: str,
) -> dict[str, str | None]:
    parsed: dict[str, str | None] = {"title": None, "content_html": None, "source_url": source_url}

    try:
        rules = _load_rules(parser_rules)
    except Exception as exc:
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=f"[run={run_id}] Invalid parser_rules detected, falling back to readability parser",
            error_stack=str(exc),
        )
        rules = None

    if rules:
        try:
            parsed.update(parse_with_rules(html, rules))
        except Exception as exc:
            await log_repo.create(
                level="WARNING",
                task_id=task_id,
                message=f"[run={run_id}] Rule-based parsing failed, falling back to readability parser",
                error_stack=str(exc),
            )

    if not parsed.get("content_html"):
        parsed.update(parse_with_readability(html))

    if not parsed.get("content_html"):
        parsed["content_html"] = html

    return parsed


def _load_rules(raw_rules: str | None) -> dict[str, object] | None:
    if not raw_rules:
        return None

    loaded = json.loads(raw_rules)
    if not isinstance(loaded, dict):
        raise ValueError("parser_rules must decode to an object")
    return loaded
