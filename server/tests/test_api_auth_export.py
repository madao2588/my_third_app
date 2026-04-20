"""Auth + CSV export routes (same app + DB as other HTTP smoke tests)."""

from fastapi.testclient import TestClient


def test_login_success_and_me(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    login = client.post(
        "/v1/auth/login",
        json={"username": "madao", "password": "666666"},
    )
    assert login.status_code == 200
    body = login.json()
    assert body.get("data") is not None
    token = body["data"]["access_token"]
    assert isinstance(token, str) and len(token) > 0

    me = client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["data"]["user"]["username"] == "madao"


def test_login_wrong_password_401(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    r = client.post(
        "/v1/auth/login",
        json={"username": "madao", "password": "wrong-password-xyz"},
    )
    assert r.status_code == 401
    payload = r.json()
    assert "message" in payload


def test_export_csv_utf8_bom_and_header(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    r = client.get("/v1/data/export/csv?limit=3")
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "text/csv" in ct
    assert "attachment" in r.headers.get("content-disposition", "")
    raw = r.content
    assert raw.startswith(b"\xef\xbb\xbf")
    assert b"id" in raw[:120]
    assert b"task_id" in raw[:120]


def test_logout_invalidates_session_then_login_ok(asgi_test_client: TestClient) -> None:
    client = asgi_test_client
    login = client.post(
        "/v1/auth/login",
        json={"username": "madao", "password": "666666"},
    )
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    out = client.post("/v1/auth/logout", headers=headers)
    assert out.status_code == 200

    me = client.get("/v1/auth/me", headers=headers)
    assert me.status_code == 401

    login2 = client.post(
        "/v1/auth/login",
        json={"username": "madao", "password": "666666"},
    )
    assert login2.status_code == 200
    token2 = login2.json()["data"]["access_token"]
    assert isinstance(token2, str) and len(token2) > 0
    me2 = client.get("/v1/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert me2.status_code == 200
