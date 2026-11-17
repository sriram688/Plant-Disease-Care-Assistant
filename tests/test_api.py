"""Integration tests for FastAPI endpoints."""

import io
from fastapi.testclient import TestClient
from PIL import Image
import pytest

from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify root greeting responds with status and project name."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "PlantGuard AI" in data["project"]
    assert data["status"] == "Online"


def test_health_endpoint():
    """Verify health endpoint returns healthy status and class count."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["classes_count"] == 9


def test_diseases_catalog():
    """Verify diseases catalog returns 9 diseases with care guidelines."""
    response = client.get("/api/diseases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    first = data[0]
    assert "class_name" in first
    assert "symptoms" in first
    assert "care" in first


def test_single_disease_valid():
    """Verify single disease lookup for tomato_early_blight."""
    response = client.get("/api/diseases/tomato_early_blight")
    assert response.status_code == 200
    data = response.json()
    assert data["plant"] == "Tomato"
    assert data["disease"] == "Early Blight"


def test_single_disease_not_found():
    """Verify 404 response for unknown disease class."""
    response = client.get("/api/diseases/unknown_plant_blight")
    assert response.status_code == 404


def test_model_info_endpoint():
    """Verify model-info endpoint returns metrics data structure."""
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "accuracy" in data
    assert "classes_count" in data


def test_predict_invalid_file_rejected():
    """Verify non-image file is rejected with 422 error."""
    file_content = b"This is not a real image"
    response = client.post(
        "/api/predict",
        files={"file": ("fake.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 422
