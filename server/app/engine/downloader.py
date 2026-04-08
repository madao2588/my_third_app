import asyncio

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


async def fetch_static(url: str) -> str:
    async def _request() -> str:
        timeout = httpx.Timeout(settings.timeout)
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers=DEFAULT_HEADERS,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    return await _with_retry(_request)


async def fetch_dynamic(url: str) -> str:
    async def _request() -> str:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto(url, timeout=settings.timeout * 1000, wait_until="domcontentloaded")
                # Add a brief explicit wait to ensure any basic async JS triggers
                await page.wait_for_timeout(2000)
                return await page.content()
            finally:
                await browser.close()

    return await _with_retry(_request)


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
