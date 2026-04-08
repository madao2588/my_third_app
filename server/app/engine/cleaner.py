import re

from bs4 import BeautifulSoup


AD_HINTS = (
    "ad",
    "ads",
    "advert",
    "banner",
    "promo",
    "sponsor",
    "popup",
    "recommend",
)


def clean_content(content_html: str | None) -> dict[str, str]:
    soup = BeautifulSoup(content_html or "", "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for tag in list(soup.find_all(_looks_like_ad_node)):
        tag.decompose()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = "\n".join(line for line in text.splitlines() if line)

    return {
        "content_html": str(soup),
        "content_text": text.strip(),
    }


def _looks_like_ad_node(tag) -> bool:
    for attr_name in ("id", "class"):
        attr_value = tag.get(attr_name)
        if not attr_value:
            continue
        values = attr_value if isinstance(attr_value, list) else [attr_value]
        joined = " ".join(values).lower()
        if any(hint in joined for hint in AD_HINTS):
            return True
    return False
