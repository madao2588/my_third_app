from collections.abc import Mapping

from bs4 import BeautifulSoup
from lxml import html as lxml_html
from readability import Document


def parse_with_rules(html: str, rules: Mapping[str, str]) -> dict[str, str | None]:
    list_item_rule = rules.get("list_item")
    fields_rule = rules.get("fields")
    if list_item_rule and isinstance(fields_rule, Mapping):
      return _parse_list_items(html, list_item_rule, fields_rule)

    title_rule = rules.get("title")
    content_rule = rules.get("content")

    title = _extract_text(html, title_rule) if title_rule else None
    content_html = _extract_html(html, content_rule) if content_rule else None

    return {
        "title": title,
        "content_html": content_html,
    }


def _parse_list_items(
    html: str,
    list_item_rule: str,
    fields_rule: Mapping[str, str],
) -> dict[str, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(list_item_rule)
    if not items:
        return {
            "title": None,
            "content_html": None,
        }

    normalized_entries: list[dict[str, str]] = []
    for item in items:
        entry: dict[str, str] = {}
        for field_name, selector in fields_rule.items():
            if not isinstance(selector, str) or not selector.strip():
                continue
            value = _extract_from_node(item, selector.strip())
            if value:
                entry[field_name] = value
        if entry:
            normalized_entries.append(entry)

    if not normalized_entries:
        return {
            "title": None,
            "content_html": None,
        }

    title = _derive_list_title(normalized_entries)
    content_html = _build_list_content_html(normalized_entries)
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


def _extract_from_node(node, selector: str) -> str | None:
    css_selector, attribute = _split_selector_and_attr(selector)
    target = node.select_one(css_selector)
    if target is None:
        return None

    if attribute is not None:
        value = target.get(attribute)
        if value is None:
            return None
        return " ".join(value) if isinstance(value, list) else str(value).strip()

    return target.get_text(" ", strip=True) or None


def _split_selector_and_attr(selector: str) -> tuple[str, str | None]:
    if "@" not in selector:
        return selector, None

    css_selector, attribute = selector.rsplit("@", 1)
    attribute = attribute.strip()
    if not css_selector.strip() or not attribute:
        return selector, None
    return css_selector.strip(), attribute


def _derive_list_title(entries: list[dict[str, str]]) -> str:
    preferred_fields = ("title", "topic", "name", "headline")
    for field in preferred_fields:
        for entry in entries:
            value = entry.get(field)
            if value:
                return value

    first_entry = entries[0]
    return next(iter(first_entry.values()), "Collected Items")


def _build_list_content_html(entries: list[dict[str, str]]) -> str:
    blocks: list[str] = []
    for index, entry in enumerate(entries[:20], start=1):
        parts = [f"<article data-index=\"{index}\">"]
        for field_name, value in entry.items():
            label = field_name.replace("_", " ").strip() or "field"
            parts.append(
                f"<p><strong>{label}:</strong> {BeautifulSoup(value, 'html.parser').get_text(' ', strip=True)}</p>"
            )
        parts.append("</article>")
        blocks.append("".join(parts))
    return "".join(blocks)
