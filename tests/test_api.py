import json

import pytest
from fastapi.testclient import TestClient
from ml_engineer_exam.api.app import app

client = TestClient(app)


def test_ping_endpoint():
    """
    Test the /ping health check endpoint
    """
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "API is running"}


def test_predict_endpoint_with_defaults():
    """
    Test the /predict endpoint using default values
    """
    response = client.post("/predict", json={})

    assert response.status_code == 200

    data = response.json()

    # Check response structure
    assert "status" in data
    assert "model_name" in data
    assert "predicted_value" in data
    assert "input_data" in data

    # Check response values
    assert data["status"] == "success"
    assert data["model_name"] == "linear"
    assert isinstance(data["predicted_value"], float)
    assert data["predicted_value"] == pytest.approx(0.719122841601914, rel=1e-6)

    # Check input_data structure
    input_data = data["input_data"]
    assert input_data["MedInc"] == 1.6812
    assert input_data["HouseAge"] == 25.0
    assert input_data["Latitude"] == 36.06
    assert input_data["Longitude"] == -119.01


def test_predict_endpoint_with_custom_input(session_fixture):
    """
    Test the /predict endpoint with custom input data
    """
    input_json = json.loads(session_fixture["input_data"])
    input_json["model_name"] = "linear"

    response = client.post("/predict", json=input_json)

    assert response.status_code == 200

    data = response.json()

    # Check response structure
    assert data["status"] == "success"
    assert data["model_name"] == "linear"
    assert isinstance(data["predicted_value"], float)
    assert data["predicted_value"] > 0


def test_predict_endpoint_response_schema():
    """
    Test that the /predict endpoint returns the exact schema format
    """
    response = client.post("/predict", json={})

    assert response.status_code == 200

    data = response.json()

    # Verify exact keys in response
    expected_keys = {"status", "model_name", "predicted_value", "input_data"}
    assert set(data.keys()) == expected_keys

    # Verify input_data has all required fields
    input_data = data["input_data"]
    expected_input_keys = {
        "model_name",
        "MedInc",
        "HouseAge",
        "AveRooms",
        "AveBedrms",
        "Population",
        "AveOccup",
        "Latitude",
        "Longitude",
    }
    assert set(input_data.keys()) == expected_input_keys


def test_train_endpoint():
    """
    Test the /train endpoint
    """
    response = client.post("/train", json={"model_name": "linear"})

    assert response.status_code == 200

    data = response.json()

    # Check response structure
    assert "status" in data
    assert "model_name" in data

    if data["status"] == "success":
        assert "metrics" in data
        assert "model_path" in data

        # Check metrics structure
        metrics = data["metrics"]
        assert "rmse" in metrics
        assert "mae" in metrics
        assert "r2" in metrics

        assert isinstance(metrics["rmse"], float)
        assert isinstance(metrics["mae"], float)
        assert isinstance(metrics["r2"], float)


def test_train_endpoint_with_different_models():
    """
    Test training different model types
    """
    model_types = ["linear", "ridge", "random_forest"]

    for model_type in model_types:
        response = client.post("/train", json={"model_name": model_type})

        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["model_name"] == model_type


def test_api_openapi_schema():
    """
    Test that the OpenAPI schema is accessible
    """
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema

    # Check that our endpoints are in the schema
    assert "/ping" in schema["paths"]
    assert "/predict" in schema["paths"]
    assert "/train" in schema["paths"]
