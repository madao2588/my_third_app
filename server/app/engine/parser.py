from collections.abc import Mapping

from bs4 import BeautifulSoup
from lxml import html as lxml_html
from readability import Document


def parse_with_rules(html: str, rules: Mapping[str, str]) -> dict[str, str | None]:
    title_rule = rules.get("title")
    content_rule = rules.get("content")

    title = _extract_text(html, title_rule) if title_rule else None
    content_html = _extract_html(html, content_rule) if content_rule else None

    return {
        "title": title,
        "content_html": content_html,
    }


def parse_with_readability(html: str) -> dict[str, str | None]:
    document = Document(html)
    title = document.short_title() or document.title()
    content_html = document.summary(html_partial=True)
    return {
        "title": title.strip() if title else None,
        "content_html": content_html,
    }


def _extract_text(html: str, selector: str) -> str | None:
    if selector.startswith("css:"):
        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one(selector.removeprefix("css:"))
        return node.get_text(" ", strip=True) if node else None

    if selector.startswith("xpath:"):
        tree = lxml_html.fromstring(html)
        nodes = tree.xpath(selector.removeprefix("xpath:"))
        if not nodes:
            return None
        node = nodes[0]
        if isinstance(node, str):
            return node.strip() or None
        return " ".join(node.itertext()).strip() or None

    raise ValueError(f"Unsupported selector format: {selector}")


def _extract_html(html: str, selector: str) -> str | None:
    if selector.startswith("css:"):
        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one(selector.removeprefix("css:"))
        return str(node) if node else None

    if selector.startswith("xpath:"):
        tree = lxml_html.fromstring(html)
        nodes = tree.xpath(selector.removeprefix("xpath:"))
        if not nodes:
            return None
        node = nodes[0]
        if isinstance(node, str):
            return node.strip() or None
        return lxml_html.tostring(node, encoding="unicode")

    raise ValueError(f"Unsupported selector format: {selector}")
