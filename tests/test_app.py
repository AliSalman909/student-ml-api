"""Automated tests for student-ml-api.

TestClient sends real requests through the FastAPI application in-process, so
no server needs to be running for these tests to execute.
"""

import pytest
from fastapi.testclient import TestClient

from app import APPLICATION_VERSION, app

client = TestClient(app)


# --- Root endpoint ---------------------------------------------------------


def test_root_returns_welcome_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Student ML API",
        "version": APPLICATION_VERSION,
    }


# --- Health endpoint -------------------------------------------------------


def test_health_returns_healthy_status():
    response = client.get("/health")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "wrong"
    assert data["application"] == "student-ml-api"
    assert data["version"] == APPLICATION_VERSION


# --- Prediction endpoint: success ------------------------------------------


def test_predict_returns_doubled_value():
    response = client.post("/predict", json={"value": 10})
    data = response.json()

    assert response.status_code == 200
    assert data["input"] == 10
    assert data["prediction"] == 20


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (7, 14),
        (-3, -6),
        (2.5, 5.0),
    ],
)
def test_predict_handles_a_range_of_numeric_inputs(value, expected):
    response = client.post("/predict", json={"value": value})

    assert response.status_code == 200
    assert response.json()["prediction"] == expected


# --- Prediction endpoint: missing input ------------------------------------


def test_predict_rejects_missing_value():
    response = client.post("/predict", json={})

    # FastAPI rejects a body that fails validation before the handler runs.
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


def test_predict_rejects_empty_body():
    response = client.post("/predict")

    assert response.status_code == 422


# --- Prediction endpoint: invalid input ------------------------------------


def test_predict_rejects_non_numeric_value():
    response = client.post("/predict", json={"value": "abc"})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "value"]


def test_predict_rejects_null_value():
    response = client.post("/predict", json={"value": None})

    assert response.status_code == 422


# --- Metadata endpoints ----------------------------------------------------


def test_model_info_returns_model_metadata():
    response = client.get("/model-info")

    assert response.status_code == 200
    assert response.json() == {
        "model_name": "double-value-model",
        "model_version": "model-1",
        "description": "Returns input multiplied by 2",
    }


def test_version_returns_application_and_model_versions():
    response = client.get("/version")
    data = response.json()

    assert response.status_code == 200
    assert data["application_version"] == APPLICATION_VERSION
    assert data["model_version"] == "model-1"


def test_version_matches_the_version_file():
    """Guards against the VERSION file and the reported version drifting apart."""
    with open("VERSION") as version_file:
        expected = version_file.read().strip()

    assert client.get("/version").json()["application_version"] == expected
