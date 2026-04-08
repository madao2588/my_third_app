from collections import Counter
from urllib.parse import urlparse


DEFAULT_NOTICE_KEYWORDS = (
    "招标",
    "采购",
    "中标",
    "原料药",
    "制剂",
    "注射液",
    "药品",
    "集采",
    "医院",
)

HIGH_PRIORITY_KEYWORDS = (
    "原料药",
    "注射液",
    "抗肿瘤",
    "集采",
    "中标",
)


def extract_source_site(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    return hostname.removeprefix("www.") or "unknown"


def extract_matched_keywords(parts: list[str | None], active_keywords: list[str]) -> list[str]:
    text = " ".join(part for part in parts if part).lower()
    return [keyword for keyword in active_keywords if keyword.lower() in text]


def is_high_priority_notice(*, quality_score: int, matched_keywords: list[str], high_priority_keywords: list[str]) -> bool:
    if quality_score >= 60:
        return True
    return any(keyword in high_priority_keywords for keyword in matched_keywords)


def build_notice_summary(content_text: str | None, max_length: int = 140) -> str:
    text = (content_text or "").strip()
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return f"{text[:max_length].rstrip()}..."


def keyword_heat_from_texts(texts: list[str], active_keywords: list[str]) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for text in texts:
        matched = extract_matched_keywords([text], active_keywords)
        counter.update(matched)
    return counter.most_common(10)
