import asyncio
import time
from collections.abc import Mapping
from urllib.parse import urlparse

import httpx
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from app.core.config import get_settings


settings = get_settings()

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

_LOGIN_STORAGE_CACHE: dict[str, tuple[float, dict[str, object]]] = {}
_LOGIN_STORAGE_CACHE_LOCK = asyncio.Lock()


async def fetch_static(
    url: str,
    *,
    headers: Mapping[str, str] | None = None,
    timeout: float | None = None,
    cookies: Mapping[str, str] | None = None,
) -> str:
    timeout_sec = float(timeout) if timeout is not None else float(settings.timeout)
    merged: dict[str, str] = dict(DEFAULT_HEADERS)
    if headers:
        merged.update(headers)

    async def _request() -> str:
        client_timeout = httpx.Timeout(timeout_sec)
        async with httpx.AsyncClient(
            timeout=client_timeout,
            follow_redirects=True,
            headers=merged,
        ) as client:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()
            return response.text

    return await _with_retry(_request)


async def fetch_dynamic(
    url: str,
    *,
    headers: Mapping[str, str] | None = None,
    timeout: float | None = None,
    cookies: Mapping[str, str] | None = None,
    cookie_domain: str | None = None,
    login_flow: Mapping[str, object] | None = None,
    proxy: Mapping[str, object] | None = None,
) -> str:
    timeout_sec = float(timeout) if timeout is not None else float(settings.timeout)
    timeout_ms = max(5_000, int(timeout_sec * 1000))

    merged: dict[str, str] = dict(DEFAULT_HEADERS)
    if headers:
        merged.update(headers)
    user_agent = merged.get("User-Agent") or DEFAULT_HEADERS["User-Agent"]
    extra_headers = {
        k: v for k, v in merged.items() if k.lower() != "user-agent"
    }

    async def _request() -> str:
        async with async_playwright() as playwright:
            launch_kwargs: dict[str, object] = {"headless": True}
            browser_proxy = _build_playwright_proxy(proxy)
            if browser_proxy is not None:
                launch_kwargs["proxy"] = browser_proxy
            browser = await playwright.chromium.launch(**launch_kwargs)
            try:
                cache_key, cache_ttl_sec = _resolve_session_cache_options(login_flow)
                cached_storage = await _get_cached_storage_state(cache_key)
                context_kwargs: dict[str, object] = {
                    "user_agent": user_agent,
                    "extra_http_headers": extra_headers or None,
                }
                if cached_storage is not None:
                    context_kwargs["storage_state"] = cached_storage
                context = await browser.new_context(**context_kwargs)
                if cookies:
                    parsed = urlparse(url)
                    if not parsed.scheme or not parsed.netloc:
                        raise ValueError("Invalid URL for cookie injection")
                    dom = (cookie_domain or "").strip()
                    if dom:
                        cookie_list = [
                            {"name": n, "value": v, "domain": dom, "path": "/"}
                            for n, v in cookies.items()
                        ]
                    else:
                        origin = f"{parsed.scheme}://{parsed.netloc}"
                        cookie_list = [
                            {"name": n, "value": v, "url": origin, "path": "/"}
                            for n, v in cookies.items()
                        ]
                    await context.add_cookies(cookie_list)
                page = await context.new_page()
                try:
                    if login_flow:
                        need_login = True
                        if cached_storage is not None:
                            need_login = not await _is_cached_login_session_valid(
                                page=page,
                                target_url=url,
                                login_flow=login_flow,
                                default_timeout_ms=timeout_ms,
                            )
                        if need_login:
                            await _run_login_flow(
                                page=page,
                                target_url=url,
                                login_flow=login_flow,
                                default_timeout_ms=timeout_ms,
                            )
                            if cache_key:
                                storage_state = await context.storage_state()
                                if isinstance(storage_state, dict):
                                    await _set_cached_storage_state(
                                        cache_key=cache_key,
                                        state=storage_state,
                                        ttl_sec=cache_ttl_sec,
                                    )
                    await page.goto(
                        url,
                        timeout=timeout_ms,
                        wait_until="domcontentloaded",
                    )
                    await page.wait_for_timeout(2000)
                    return await page.content()
                finally:
                    await page.close()
                    await context.close()
            finally:
                await browser.close()

    return await _with_retry(_request)


def _build_playwright_proxy(proxy: Mapping[str, object] | None) -> dict[str, str] | None:
    if proxy is None:
        return None
    server = proxy.get("server")
    if not isinstance(server, str) or not server.strip():
        return None
    out: dict[str, str] = {"server": server.strip()}
    username = proxy.get("username")
    password = proxy.get("password")
    if isinstance(username, str) and username:
        out["username"] = username
    if isinstance(password, str) and password:
        out["password"] = password
    return out


def _resolve_session_cache_options(
    login_flow: Mapping[str, object] | None,
) -> tuple[str | None, int]:
    if login_flow is None:
        return None, 1800
    cache_key_raw = login_flow.get("session_key")
    cache_key = (
        cache_key_raw.strip()[:128]
        if isinstance(cache_key_raw, str) and cache_key_raw.strip()
        else None
    )
    ttl_raw = login_flow.get("session_ttl_sec")
    ttl_sec = 1800
    if isinstance(ttl_raw, (int, float)):
        ttl_sec = int(ttl_raw)
    ttl_sec = max(60, min(86_400, ttl_sec))
    return cache_key, ttl_sec


async def _get_cached_storage_state(cache_key: str | None) -> dict[str, object] | None:
    if not cache_key:
        return None
    now = time.monotonic()
    async with _LOGIN_STORAGE_CACHE_LOCK:
        item = _LOGIN_STORAGE_CACHE.get(cache_key)
        if item is None:
            return None
        expires_at, state = item
        if expires_at <= now:
            _LOGIN_STORAGE_CACHE.pop(cache_key, None)
            return None
        return dict(state)


async def _set_cached_storage_state(
    *,
    cache_key: str,
    state: dict[str, object],
    ttl_sec: int,
) -> None:
    if not cache_key:
        return
    expires_at = time.monotonic() + ttl_sec
    async with _LOGIN_STORAGE_CACHE_LOCK:
        _LOGIN_STORAGE_CACHE[cache_key] = (expires_at, dict(state))


async def _is_cached_login_session_valid(
    *,
    page,
    target_url: str,
    login_flow: Mapping[str, object],
    default_timeout_ms: int,
) -> bool:
    check_selector = login_flow.get("session_check_selector")
    if not isinstance(check_selector, str) or not check_selector.strip():
        return True
    check_url_raw = login_flow.get("session_check_url")
    check_url = (
        check_url_raw.strip()
        if isinstance(check_url_raw, str) and check_url_raw.strip()
        else target_url
    )
    timeout_ms = _bounded_timeout(login_flow.get("timeout_ms"), default_timeout_ms)
    timeout_ms = min(timeout_ms, 6_000)
    try:
        await page.goto(
            check_url,
            timeout=timeout_ms,
            wait_until="domcontentloaded",
        )
        await page.wait_for_selector(check_selector.strip(), timeout=timeout_ms)
        return True
    except (PlaywrightTimeoutError, PlaywrightError):
        return False


async def _run_login_flow(
    *,
    page,
    target_url: str,
    login_flow: Mapping[str, object],
    default_timeout_ms: int,
) -> None:
    flow_timeout = _bounded_timeout(login_flow.get("timeout_ms"), default_timeout_ms)
    login_url = login_flow.get("url")
    if isinstance(login_url, str) and login_url.strip():
        await page.goto(
            login_url.strip(),
            timeout=flow_timeout,
            wait_until="domcontentloaded",
        )
    else:
        await page.goto(
            target_url,
            timeout=flow_timeout,
            wait_until="domcontentloaded",
        )

    values_raw = login_flow.get("values")
    values: Mapping[str, str] = values_raw if isinstance(values_raw, Mapping) else {}
    steps_raw = login_flow.get("steps")
    if not isinstance(steps_raw, list):
        return

    for step_raw in steps_raw:
        if not isinstance(step_raw, Mapping):
            continue
        action = str(step_raw.get("action") or "").strip().lower()
        timeout_ms = _bounded_timeout(step_raw.get("timeout_ms"), flow_timeout)
        if action == "goto":
            step_url = step_raw.get("url")
            if isinstance(step_url, str) and step_url.strip():
                await page.goto(
                    step_url.strip(),
                    timeout=timeout_ms,
                    wait_until="domcontentloaded",
                )
            continue
        if action == "fill":
            selector = step_raw.get("selector")
            if not isinstance(selector, str) or not selector.strip():
                raise ValueError("login_flow fill step requires selector")
            value = ""
            value_from = step_raw.get("value_from")
            if isinstance(value_from, str) and value_from in values:
                value = values[value_from]
            elif isinstance(step_raw.get("value"), str):
                value = str(step_raw.get("value"))
            await page.fill(selector.strip(), value, timeout=timeout_ms)
            continue
        if action == "click":
            selector = step_raw.get("selector")
            if not isinstance(selector, str) or not selector.strip():
                raise ValueError("login_flow click step requires selector")
            await page.click(selector.strip(), timeout=timeout_ms)
            continue
        if action == "wait_for_selector":
            selector = step_raw.get("selector")
            if not isinstance(selector, str) or not selector.strip():
                raise ValueError("login_flow wait_for_selector step requires selector")
            await page.wait_for_selector(selector.strip(), timeout=timeout_ms)
            continue
        if action == "wait_for_load_state":
            wait_until = str(step_raw.get("wait_until") or "networkidle").strip().lower()
            if wait_until not in {"load", "domcontentloaded", "networkidle"}:
                wait_until = "networkidle"
            await page.wait_for_load_state(wait_until, timeout=timeout_ms)
            continue
        if action == "sleep":
            ms_raw = step_raw.get("ms")
            ms = 0
            if isinstance(ms_raw, (int, float)):
                ms = int(ms_raw)
            await page.wait_for_timeout(max(0, min(60_000, ms)))
            continue

    success_selector = login_flow.get("success_selector")
    if isinstance(success_selector, str) and success_selector.strip():
        await page.wait_for_selector(success_selector.strip(), timeout=flow_timeout)


def _bounded_timeout(raw_value: object, default_timeout: int) -> int:
    if isinstance(raw_value, (int, float)):
        return max(1_000, min(60_000, int(raw_value)))
    return max(1_000, min(60_000, int(default_timeout)))


async def _with_retry(operation, retries: int | None = None) -> str:
    max_retries = retries or settings.max_retry
    last_exception: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            return await operation()
        except (httpx.HTTPError, PlaywrightTimeoutError, PlaywrightError, RuntimeError) as exc:
            last_exception = exc
            if attempt == max_retries:
                break
            await asyncio.sleep(min(attempt, 3))

    assert last_exception is not None
    raise last_exception
