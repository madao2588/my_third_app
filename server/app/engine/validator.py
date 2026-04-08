import re


def quality_score(title: str | None, content_text: str | None) -> int:
    text = (content_text or "").strip()
    score = 0

    if title and title.strip():
        score += 20

    if len(text) > 200:
        score += 30

    if _has_no_garbled_text(text):
        score += 20

    if _has_complete_structure(title, text):
        score += 30

    return min(score, 100)


def _has_no_garbled_text(text: str) -> bool:
    if not text:
        return False
    if "\ufffd" in text or "�" in text:
        return False

    suspicious = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text)
    return len(suspicious) == 0


def _has_complete_structure(title: str | None, content_text: str) -> bool:
    return bool(title and title.strip() and len(content_text.strip()) >= 80)
