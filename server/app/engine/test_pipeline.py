import json
import traceback

from app.engine.cleaner import clean_content
from app.engine.downloader import fetch_dynamic, fetch_static
from app.engine.parser import parse_with_readability, parse_with_rules
from app.engine.validator import quality_score

async def test_run(start_url: str, parser_rules: str | None = None) -> dict:
    try:
        try:
            html = await fetch_static(start_url)
        except Exception:
            html = await fetch_dynamic(start_url)

        parsed: dict[str, str | None] = {"title": None, "content_html": None, "source_url": start_url}

        rules = None
        if parser_rules:
            try:
                loaded = json.loads(parser_rules)
                if isinstance(loaded, dict):
                    rules = loaded
            except Exception:
                pass
        
        if rules:
            try:
                parsed_rules_res = parse_with_rules(html, rules)
                parsed.update(parsed_rules_res)
            except Exception:
                pass

        if not parsed.get("content_html"):
            try:
                parsed_readability = parse_with_readability(html)
                parsed.update(parsed_readability)
            except Exception:
                pass
            
        if not parsed.get("content_html"):
            parsed["content_html"] = html
            
        cleaned = clean_content(parsed["content_html"])
        score = quality_score(parsed.get("title"), cleaned["content_text"])
        
        return {
            "title": parsed.get("title"),
            "content_text": cleaned["content_text"],
            "content_html": cleaned["content_html"],
            "quality_score": score,
            "error": None
        }
    except Exception:
        return {
            "title": None,
            "content_text": None,
            "content_html": None,
            "quality_score": None,
            "error": traceback.format_exc()
        }