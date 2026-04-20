from app.services.data_service import parse_run_summary_from_log


def test_parse_run_summary_list_follow_with_run_id() -> None:
    msg = (
        "[run=abc123] list_follow summary: list_pages=2, detail_discovered=12, "
        "stored=7, skipped_hash=3, failed=2, detail_limit_hit=true"
    )
    parsed = parse_run_summary_from_log(
        message=msg,
        run_summary=None,
        error_stack=None,
    )
    assert parsed is not None
    assert parsed.run_id == "abc123"
    assert parsed.mode == "list_follow"
    assert parsed.metrics["list_pages"] == 2
    assert parsed.metrics["stored"] == 7
    assert parsed.metrics["detail_limit_hit"] is True


def test_parse_run_summary_single_page_without_run_id() -> None:
    msg = "single_page summary: processed=1, stored=0, skipped_hash=1, failed=0"
    parsed = parse_run_summary_from_log(
        message=msg,
        run_summary=None,
        error_stack=None,
    )
    assert parsed is not None
    assert parsed.run_id is None
    assert parsed.mode == "single_page"
    assert parsed.metrics == {
        "processed": 1,
        "stored": 0,
        "skipped_hash": 1,
        "failed": 0,
    }


def test_parse_run_summary_non_summary_message_returns_none() -> None:
    assert (
        parse_run_summary_from_log(
            message="Task 1 execution finished",
            run_summary=None,
            error_stack=None,
        )
        is None
    )


def test_parse_run_summary_prefers_structured_error_stack() -> None:
    parsed = parse_run_summary_from_log(
        message="[run=zzz] single_page summary: processed=1, stored=1",
        run_summary='{"kind":"run_summary","run_id":"abc","mode":"single_page","metrics":{"processed":1,"stored":1}}',
        error_stack=None,
    )
    assert parsed is not None
    assert parsed.run_id == "abc"
    assert parsed.mode == "single_page"
    assert parsed.metrics["processed"] == 1


def test_parse_run_summary_fallback_to_error_stack_for_legacy_rows() -> None:
    parsed = parse_run_summary_from_log(
        message="[run=legacy] single_page summary: processed=1, stored=1",
        run_summary=None,
        error_stack='{"kind":"run_summary","run_id":"legacy","mode":"single_page","metrics":{"processed":1}}',
    )
    assert parsed is not None
    assert parsed.run_id == "legacy"
