import json
import traceback
from collections.abc import Mapping

from app.core.database import AsyncSessionLocal
from app.engine.cleaner import clean_content
from app.engine.downloader import fetch_dynamic, fetch_static
from app.engine.parser import parse_with_readability, parse_with_rules
from app.engine.validator import quality_score
from app.repositories.data_repo import DataRepository
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskStatus
from app.utils.file import save_snapshot
from app.utils.hash import sha256_text


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

        try:
            html = await _download_page(url=task.start_url, log_repo=log_repo, task_id=task_id)
            parsed = await _parse_page(
                html,
                parser_rules=task.parser_rules,
                source_url=task.start_url,
                log_repo=log_repo,
                task_id=task_id,
            )
            cleaned = clean_content(parsed["content_html"])
            score = quality_score(parsed.get("title"), cleaned["content_text"])

            if score < 40:
                await log_repo.create(
                    level="WARNING",
                    task_id=task_id,
                    message=f"Task {task_id} produced low quality content: {score}",
                )

            content_hash = sha256_text(cleaned["content_text"])
            duplicate = await data_repo.get_by_hash(content_hash)
            if duplicate is not None:
                await log_repo.create(
                    level="INFO",
                    task_id=task_id,
                    message=f"Duplicate content detected for task {task_id}, skipping storage",
                )
                return

            existing = await data_repo.get_by_source_url(task.start_url)
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
                    source_url=task.start_url,
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
                    message=f"Snapshot save failed for data {stored.id}",
                    error_stack=str(exc),
                )

            await log_repo.create(
                level="INFO",
                task_id=task_id,
                message=f"Task {task_id} collected data item {stored.id}",
            )
        except Exception as exc:
            await log_repo.create(
                level="ERROR",
                task_id=task_id,
                message=f"Task {task_id} pipeline execution failed",
                error_stack=traceback.format_exc(),
            )
            raise


async def _download_page(*, task_id: int, log_repo: LogRepository, url: str) -> str:
    try:
        return await fetch_static(url)
    except Exception as static_exc:
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message=f"Static fetch failed for {url}, falling back to dynamic fetch",
            error_stack=str(static_exc),
        )
        return await fetch_dynamic(url)


async def _parse_page(
    html: str,
    *,
    parser_rules: str | None,
    source_url: str,
    log_repo: LogRepository,
    task_id: int,
) -> dict[str, str | None]:
    parsed: dict[str, str | None] = {"title": None, "content_html": None, "source_url": source_url}

    try:
        rules = _load_rules(parser_rules)
    except Exception as exc:
        await log_repo.create(
            level="WARNING",
            task_id=task_id,
            message="Invalid parser_rules detected, falling back to readability parser",
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
                message="Rule-based parsing failed, falling back to readability parser",
                error_stack=str(exc),
            )

    if not parsed.get("content_html"):
        parsed.update(parse_with_readability(html))

    if not parsed.get("content_html"):
        parsed["content_html"] = html

    return parsed


def _load_rules(raw_rules: str | None) -> Mapping[str, str] | None:
    if not raw_rules:
        return None

    loaded = json.loads(raw_rules)
    if not isinstance(loaded, dict):
        raise ValueError("parser_rules must decode to an object")
    return loaded
