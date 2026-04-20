import pytest

from app.schemas.parser_rules import validate_parser_rules_str


def test_validate_parser_rules_accepts_object_and_empty() -> None:
    assert validate_parser_rules_str(None) is None
    assert validate_parser_rules_str("  ") is None
    assert validate_parser_rules_str('{"a": 1}') == '{"a": 1}'


def test_validate_parser_rules_rejects_non_object_root() -> None:
    with pytest.raises(ValueError, match="object"):
        validate_parser_rules_str("[1,2]")


def test_validate_parser_rules_rejects_invalid_json() -> None:
    with pytest.raises(ValueError, match="JSON"):
        validate_parser_rules_str("{not json")
