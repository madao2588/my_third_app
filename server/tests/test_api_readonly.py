"""Read-only v1 endpoints (shared session-scoped ASGI client)."""

from fastapi.testclient import TestClient


def test_log_summary_shape(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/logs/summary")
    assert r.status_code == 200
    data = r.json()["data"]
    for key in (
        "total_logs",
        "info_logs",
        "warning_logs",
        "error_logs",
        "failed_task_count",
    ):
        assert key in data
        assert isinstance(data[key], int)


def test_logs_list_paginated(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get(
        "/v1/logs",
        params={"page": 1, "page_size": 5},
    )
    assert r.status_code == 200
    body = r.json()["data"]
    assert "items" in body
    assert "total" in body
    assert isinstance(body["items"], list)
    if body["items"]:
        first = body["items"][0]
        assert "run_summary" in first


def test_logs_list_only_summary_filter(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get(
        "/v1/logs",
        params={"page": 1, "page_size": 20, "only_summary": "true"},
    )
    assert r.status_code == 200
    body = r.json()["data"]
    assert "items" in body
    assert "total" in body
    for item in body["items"]:
        msg = (item.get("message") or "").lower()
        has_struct = item.get("run_summary") is not None
        looks_legacy_summary = (" summary:" in msg) or ("运行摘要" in msg)
        assert has_struct or looks_legacy_summary


def test_dashboard_overview_shape(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/dashboard/overview")
    assert r.status_code == 200
    data = r.json()["data"]
    assert "metrics" in data
    assert "runtime" in data
    assert "high_value_notices" in data
    assert "recent_notices" in data
    rt = data["runtime"]
    assert rt["status"] in ("ok", "degraded")
    assert rt["database"] in ("ok", "error")


def test_keyword_rules_list(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/keywords")
    assert r.status_code == 200
    data = r.json()["data"]
    assert "items" in data
    assert "total" in data


def test_task_templates_list(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/templates/tasks")
    assert r.status_code == 200
    data = r.json()["data"]
    assert isinstance(data, list)


def test_notices_list_paginated(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get(
        "/v1/notices",
        params={"page": 1, "page_size": 10, "keyword": ""},
    )
    assert r.status_code == 200
    body = r.json()["data"]
    assert "items" in body
    assert "total" in body
    assert isinstance(body["items"], list)


def test_stats_overview_shape(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/stats/overview")
    assert r.status_code == 200
    data = r.json()["data"]
    for key in (
        "total_tasks",
        "enabled_tasks",
        "total_data",
        "today_data",
        "total_logs",
        "avg_quality_score",
    ):
        assert key in data


def test_notice_detail_missing_returns_404(asgi_test_client: TestClient) -> None:
    r = asgi_test_client.get("/v1/notices/999999999")
    assert r.status_code == 404
    assert "message" in r.json()
