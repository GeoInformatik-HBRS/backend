from fastapi.testclient import TestClient

from src.bootstrap.application import create_app


def test_health() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_local_vite_origin() -> None:
    with TestClient(create_app()) as client:
        response = client.get(
            "/health", headers={"Origin": "http://localhost:5173"}
        )

    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:5173"
    )


def test_cors_rejects_unknown_origin() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health", headers={"Origin": "http://example.com"})

    assert "access-control-allow-origin" not in response.headers
