from fastapi.testclient import TestClient

from src.main import create_app


def test_login_and_protected_endpoint() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    token = data["access_token"]
    protected = client.get(
        "/protected/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert protected.status_code == 200
    assert protected.json()["user"] == "admin"


def test_missing_token() -> None:
    client = TestClient(create_app())
    response = client.get("/protected/me")
    assert response.status_code == 401
