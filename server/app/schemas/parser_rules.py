"""Shared validation for task / template ``parser_rules`` JSON strings."""

from __future__ import annotations

import json


def validate_parser_rules_str(value: str | None) -> str | None:
    """Require valid JSON with an object at the root when non-empty."""
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ValueError(f"parser_rules must be valid JSON ({exc})") from exc
    if not isinstance(parsed, dict):
        raise ValueError("parser_rules must be a JSON object at the root")
    return value
