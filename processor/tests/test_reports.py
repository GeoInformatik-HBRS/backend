from fastapi.testclient import TestClient

from src.bootstrap.application import create_app

def test_create_report_with_supported_category_returns_204() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/reports", json={"category": "overflowing_public_bin"})
    
    assert response.status_code == 204


def test_create_report_with_unknown_category_returns_400() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/reports", json={"category": "unknown_category"})
        
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported category"}


def test_create_report_without_required_data_returns_422() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/reports", json={})
        
    assert response.status_code == 422


def test_create_report_with_category_other_returns_204() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/reports", json={"category": "other"})
        
    assert response.status_code == 204
