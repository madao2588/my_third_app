"""HTTP smoke against the real ASGI app (lifespan runs init_db, scheduler, bootstrap)."""

from fastapi.testclient import TestClient


def test_health_and_tasks_list_smoke(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    health = client.get("/health")
    assert health.status_code == 200
    payload = health.json()
    assert payload.get("data") is not None
    assert payload["data"]["status"] in ("ok", "degraded")
    assert payload["data"]["database"] in ("ok", "error")
    assert payload["data"]["scheduler"] in ("running", "stopped")

    tasks = client.get(
        "/v1/tasks",
        params={"page": 1, "page_size": 1},
    )
    assert tasks.status_code == 200
    body = tasks.json()
    assert body.get("data") is not None
    assert "items" in body["data"]
    assert "total" in body["data"]
