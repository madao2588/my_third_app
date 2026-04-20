import json
import traceback
from typing import Any

from app.engine.cleaner import clean_content
from app.engine.downloader import fetch_dynamic, fetch_static
from app.engine.parser import parse_with_readability, parse_with_rules
from app.engine.pipeline import _load_rules
from app.engine.validator import quality_score


async def test_run(start_url: str, parser_rules: str | None = None) -> dict[str, Any]:
    notes: list[str] = []
    fetch_mode: str | None = None
    content_source: str | None = None

    try:
        html: str
        try:
            html = await fetch_static(start_url)
            fetch_mode = "static"
        except Exception as static_exc:
            notes.append(f"静态抓取失败，已回退动态抓取：{static_exc!s}")
            html = await fetch_dynamic(start_url)
            fetch_mode = "dynamic"

        parsed: dict[str, str | None] = {
            "title": None,
            "content_html": None,
            "source_url": start_url,
        }

        rules = None
        try:
            rules = _load_rules(parser_rules)
        except json.JSONDecodeError as exc:
            notes.append(f"parser_rules 不是合法 JSON：{exc!s}")
        except ValueError as exc:
            notes.append(str(exc))
        except Exception as exc:
            notes.append(f"解析 parser_rules 失败：{exc!s}")

        if rules:
            try:
                parsed_rules_res = parse_with_rules(html, rules)
                parsed.update(parsed_rules_res)
                if parsed.get("content_html"):
                    content_source = "rules"
            except Exception as exc:
                notes.append(f"规则解析失败，将尝试正文抽取：{exc!s}")

        if not parsed.get("content_html"):
            try:
                parsed_readability = parse_with_readability(html)
                parsed.update(parsed_readability)
                if parsed.get("content_html"):
                    content_source = "readability"
            except Exception as exc:
                notes.append(f"readability 抽取失败：{exc!s}")

        if not parsed.get("content_html"):
            parsed["content_html"] = html
            content_source = "raw_html"
            notes.append("未得到有效正文 HTML，已退回原始 HTML。")

        cleaned = clean_content(parsed["content_html"])
        score = quality_score(parsed.get("title"), cleaned["content_text"])

        trace = {
            "fetch": fetch_mode,
            "content_source": content_source,
            "notes": notes,
        }

        return {
            "title": parsed.get("title"),
            "content_text": cleaned["content_text"],
            "content_html": cleaned["content_html"],
            "quality_score": score,
            "error": None,
            "trace": trace,
        }
    except Exception:
        return {
            "title": None,
            "content_text": None,
            "content_html": None,
            "quality_score": None,
            "error": traceback.format_exc(),
            "trace": {
                "fetch": fetch_mode,
                "content_source": content_source,
                "notes": notes,
            },
        }
