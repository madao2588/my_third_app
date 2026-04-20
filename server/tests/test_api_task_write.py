"""Task create / read / delete via HTTP (shared ASGI client)."""

import asyncio
import time
import uuid

import app.engine.pipeline as pipeline_mod
from fastapi.testclient import TestClient


def test_create_task_get_and_delete(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    name = f"pytest_task_{suffix}"
    body = {
        "name": name,
        "start_url": "https://example.com/pytest-task",
        "cron_expr": "0 0 * * *",
        "status": 1,
        "parser_rules": None,
    }
    created = client.post("/v1/tasks", json=body)
    assert created.status_code == 200
    payload = created.json()
    assert payload.get("data") is not None
    data = payload["data"]
    assert data["name"] == name
    assert data["start_url"] == body["start_url"]
    task_id = data["id"]
    assert isinstance(task_id, int) and task_id > 0

    fetched = client.get(f"/v1/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["data"]["id"] == task_id
    assert fetched.json()["data"]["name"] == name

    deleted = client.delete(f"/v1/tasks/{task_id}")
    assert deleted.status_code == 200

    missing = client.get(f"/v1/tasks/{task_id}")
    assert missing.status_code == 404


def test_put_task_update_name(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    name = f"pytest_put_{suffix}"
    created = client.post(
        "/v1/tasks",
        json={
            "name": name,
            "start_url": "https://example.com/put",
            "cron_expr": "0 0 * * *",
            "status": 1,
        },
    )
    assert created.status_code == 200
    task_id = created.json()["data"]["id"]
    updated_name = f"{name}_renamed"
    put = client.put(
        f"/v1/tasks/{task_id}",
        json={"name": updated_name},
    )
    assert put.status_code == 200
    assert put.json()["data"]["name"] == updated_name
    assert client.get(f"/v1/tasks/{task_id}").json()["data"]["name"] == updated_name
    assert client.delete(f"/v1/tasks/{task_id}").status_code == 200


async def _slow_pipeline_run(_task_id: int) -> None:
    await asyncio.sleep(1.0)


async def _instant_pipeline_run(_task_id: int) -> None:
    return


def test_post_run_task_returns_queued(
    asgi_test_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setattr(pipeline_mod, "run_task", _instant_pipeline_run)
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    name = f"pytest_run_{suffix}"
    created = client.post(
        "/v1/tasks",
        json={
            "name": name,
            "start_url": "https://example.com/run",
            "cron_expr": "0 0 * * *",
            "status": 1,
        },
    )
    assert created.status_code == 200
    task_id = created.json()["data"]["id"]
    run = client.post(f"/v1/tasks/{task_id}/run")
    assert run.status_code == 200
    payload = run.json()["data"]
    assert payload["task_id"] == task_id
    assert payload["status"] == "queued"
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        status = client.get(f"/v1/tasks/{task_id}").json()["data"]["last_run_status"]
        if status not in ("queued", "running"):
            break
        time.sleep(0.05)
    assert client.delete(f"/v1/tasks/{task_id}").status_code == 200


def test_delete_task_rejected_while_queued_or_running(
    asgi_test_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setattr(pipeline_mod, "run_task", _slow_pipeline_run)
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    name = f"pytest_del_{suffix}"
    created = client.post(
        "/v1/tasks",
        json={
            "name": name,
            "start_url": "https://example.com/delbusy",
            "cron_expr": "0 0 * * *",
            "status": 1,
        },
    )
    assert created.status_code == 200
    task_id = created.json()["data"]["id"]
    assert client.post(f"/v1/tasks/{task_id}/run").status_code == 200
    assert client.delete(f"/v1/tasks/{task_id}").status_code == 409
    time.sleep(1.2)
    assert client.delete(f"/v1/tasks/{task_id}").status_code == 200


def test_post_run_task_conflict_409_while_active(
    asgi_test_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setattr(pipeline_mod, "run_task", _slow_pipeline_run)
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    name = f"pytest_run2_{suffix}"
    created = client.post(
        "/v1/tasks",
        json={
            "name": name,
            "start_url": "https://example.com/run2",
            "cron_expr": "0 0 * * *",
            "status": 1,
        },
    )
    assert created.status_code == 200
    task_id = created.json()["data"]["id"]
    first = client.post(f"/v1/tasks/{task_id}/run")
    assert first.status_code == 200
    second = client.post(f"/v1/tasks/{task_id}/run")
    assert second.status_code == 409
    time.sleep(1.2)
    assert client.delete(f"/v1/tasks/{task_id}").status_code == 200


def test_create_task_parser_rules_invalid_json_rejected(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    r = client.post(
        "/v1/tasks",
        json={
            "name": f"pytest_badjson_{suffix}",
            "start_url": "https://example.com/badjson",
            "cron_expr": "0 0 * * *",
            "status": 1,
            "parser_rules": "{",
        },
    )
    assert r.status_code == 422


def test_create_task_parser_rules_array_root_rejected(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    r = client.post(
        "/v1/tasks",
        json={
            "name": f"pytest_arr_{suffix}",
            "start_url": "https://example.com/arr",
            "cron_expr": "0 0 * * *",
            "status": 1,
            "parser_rules": "[1]",
        },
    )
    assert r.status_code == 422


def test_create_task_parser_rules_too_long_rejected(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    suffix = uuid.uuid4().hex[:10]
    huge = "x" * 200_000
    r = client.post(
        "/v1/tasks",
        json={
            "name": f"pytest_big_{suffix}",
            "start_url": "https://example.com/big",
            "cron_expr": "0 0 * * *",
            "status": 1,
            "parser_rules": huge,
        },
    )
    assert r.status_code == 422


def test_list_data_paginated(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    r = client.get("/v1/data", params={"page": 1, "page_size": 5})
    assert r.status_code == 200
    body = r.json()["data"]
    assert "items" in body
    assert "total" in body
    assert isinstance(body["items"], list)
