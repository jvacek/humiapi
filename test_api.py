#!/usr/bin/env python3
"""
Pytest test suite for FastAPI application functionality.
"""

import time
from threading import Thread

import pytest
import requests
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def live_server():
    """Start a live server for integration tests."""
    import uvicorn

    def run_app():
        uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="error")

    server_thread = Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(3)  # Wait for server to start
    yield "http://127.0.0.1:8002"


class TestHealthEndpoint:
    """Test the health check endpoints."""

    def test_api_health_check(self, client):
        """Test /api/health endpoint returns success."""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.json()
        assert data == {"status": "healthy"}

    def test_health_check_alt(self, client):
        """Test /health endpoint returns success."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data == {"status": "healthy"}

    def test_health_check_live(self, live_server):
        """Test health endpoint on live server."""
        response = requests.get(f"{live_server}/api/health", timeout=5)
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestWebInterface:
    """Test the web interface."""

    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200

        content = response.text
        assert "Absolute Humidity Calculator" in content
        assert "Temperature" in content
        assert "Humidity" in content

    def test_home_page_contains_form(self, client):
        """Test that the home page contains the calculation form."""
        response = client.get("/")
        content = response.text

        assert 'id="temperature"' in content
        assert 'id="humidity"' in content
        assert 'type="submit"' in content

    def test_home_page_has_examples(self, client):
        """Test that the home page contains example values."""
        response = client.get("/")
        content = response.text

        assert "Quick Examples" in content
        assert "Room Comfort" in content
        assert "setValues" in content  # JavaScript function for examples


class TestCalculationEndpoint:
    """Test the calculation API endpoint."""

    def test_successful_calculation(self, client):
        """Test successful calculation with valid inputs."""
        data = {"temperature": 25.5, "humidity": 60}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        result = response.json()

        assert "absolute_humidity" in result
        assert "temperature" in result
        assert "humidity" in result
        assert "unit" in result

        assert result["temperature"] == 25.5
        assert result["humidity"] == 60
        assert result["unit"] == "g/m³"
        assert isinstance(result["absolute_humidity"], (int, float))
        assert result["absolute_humidity"] > 0

    @pytest.mark.parametrize(
        "temp,humidity,expected_range",
        [
            (20.0, 50, (8.0, 9.0)),
            (30.0, 80, (24.0, 25.0)),
            (0.0, 30, (1.0, 2.0)),
            (25.0, 0, (0.0, 0.0)),
            (25.0, 100, (22.0, 24.0)),
        ],
    )
    def test_calculation_values(self, client, temp, humidity, expected_range):
        """Test calculation returns expected values for known inputs."""
        data = {"temperature": temp, "humidity": humidity}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        result = response.json()

        abs_humidity = result["absolute_humidity"]
        min_expected, max_expected = expected_range

        assert min_expected <= abs_humidity <= max_expected, (
            f"Expected {min_expected}-{max_expected}, got {abs_humidity} for {temp}°C, {humidity}% RH"
        )

    def test_decimal_temperature(self, client):
        """Test that decimal temperatures are handled correctly."""
        data = {"temperature": 22.7, "humidity": 55}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        result = response.json()
        assert result["temperature"] == 22.7

    def test_calculation_live_server(self, live_server):
        """Test calculation endpoint on live server."""
        data = {"temperature": 25.0, "humidity": 60}
        response = requests.post(
            f"{live_server}/api/calculate",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code == 200
        result = response.json()
        assert "absolute_humidity" in result
        assert result["absolute_humidity"] > 0

    def test_integer_temperature(self, client):
        """Test that integer temperatures work correctly."""
        data = {"temperature": 25, "humidity": 60}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        result = response.json()
        assert result["temperature"] == 25.0  # Should be converted to float


class TestErrorHandling:
    """Test error handling and validation."""

    def test_missing_temperature(self, client):
        """Test error when temperature is missing."""
        data = {"humidity": 50}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422  # Unprocessable Entity
        error = response.json()
        assert "detail" in error

    def test_missing_humidity(self, client):
        """Test error when humidity is missing."""
        data = {"temperature": 25.0}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422  # Unprocessable Entity
        error = response.json()
        assert "detail" in error

    def test_missing_both_parameters(self, client):
        """Test error when both parameters are missing."""
        data = {}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422  # Unprocessable Entity
        error = response.json()
        assert "detail" in error

    def test_invalid_humidity_too_high(self, client):
        """Test error when humidity is above 100%."""
        data = {"temperature": 25.0, "humidity": 101}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422  # Unprocessable Entity
        error = response.json()
        assert "detail" in error

    def test_invalid_humidity_negative(self, client):
        """Test error when humidity is negative."""
        data = {"temperature": 25.0, "humidity": -10}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422  # Unprocessable Entity
        error = response.json()
        assert "detail" in error

    @pytest.mark.parametrize("invalid_humidity", [-1, 101, 150, -50])
    def test_humidity_range_validation(self, client, invalid_humidity):
        """Test that invalid humidity values are rejected."""
        data = {"temperature": 25.0, "humidity": invalid_humidity}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422

    def test_invalid_temperature_type(self, client):
        """Test error when temperature is not a number."""
        data = {"temperature": "not_a_number", "humidity": 50}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422
        error = response.json()
        assert "detail" in error

    def test_invalid_humidity_type(self, client):
        """Test error when humidity is not a number."""
        data = {"temperature": 25.0, "humidity": "not_a_number"}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422
        error = response.json()
        assert "detail" in error

    def test_no_json_data(self, client):
        """Test error when no JSON data is provided."""
        response = client.post("/api/calculate")

        assert response.status_code == 422

    def test_invalid_json(self, client):
        """Test error when invalid JSON is provided."""
        response = client.post(
            "/api/calculate",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    def test_empty_json(self, client):
        """Test error when empty JSON object is provided."""
        response = client.post("/api/calculate", json={})

        assert response.status_code == 422

    def test_null_values(self, client):
        """Test error when null values are provided."""
        data = {"temperature": None, "humidity": None}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422


class TestResponseFormat:
    """Test the format of API responses."""

    def test_successful_response_structure(self, client):
        """Test that successful responses have the correct structure."""
        data = {"temperature": 25.0, "humidity": 60}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        result = response.json()

        # Check all required fields are present
        required_fields = ["absolute_humidity", "temperature", "humidity", "unit"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"

        # Check data types
        assert isinstance(result["absolute_humidity"], (int, float))
        assert isinstance(result["temperature"], (int, float))
        assert isinstance(result["humidity"], int)
        assert isinstance(result["unit"], str)

        # Check unit is correct
        assert result["unit"] == "g/m³"

    def test_error_response_structure(self, client):
        """Test that error responses have the correct structure."""
        data = {"temperature": 25.0, "humidity": 101}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 422
        error = response.json()

        assert "detail" in error
        assert isinstance(error["detail"], (str, list))

    def test_content_type_headers(self, client):
        """Test that responses have correct content type."""
        data = {"temperature": 25.0, "humidity": 60}
        response = client.post("/api/calculate", json=data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"


class TestHttpMethods:
    """Test HTTP method restrictions."""

    def test_get_not_allowed_on_calculate(self, client):
        """Test that GET is not allowed on calculate endpoint."""
        response = client.get("/api/calculate")
        assert response.status_code == 405  # Method Not Allowed

    def test_put_not_allowed_on_calculate(self, client):
        """Test that PUT is not allowed on calculate endpoint."""
        response = client.put("/api/calculate")
        assert response.status_code == 405  # Method Not Allowed

    def test_delete_not_allowed_on_calculate(self, client):
        """Test that DELETE is not allowed on calculate endpoint."""
        response = client.delete("/api/calculate")
        assert response.status_code == 405  # Method Not Allowed

    def test_post_not_allowed_on_health(self, client):
        """Test that POST is not allowed on health endpoint."""
        response = client.post("/api/health")
        assert response.status_code == 405  # Method Not Allowed


class TestDocumentation:
    """Test API documentation endpoints."""

    def test_openapi_docs_available(self, client):
        """Test that OpenAPI docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_redoc_available(self, client):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()

    def test_openapi_json(self, client):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "info" in openapi_spec
        assert "paths" in openapi_spec


class TestValidationEdgeCases:
    """Test edge cases for input validation."""

    def test_very_large_temperature(self, client):
        """Test with very large temperature value."""
        data = {"temperature": 1000.0, "humidity": 50}
        response = client.post("/api/calculate", json=data)

        # Should not fail validation but might produce large result
        assert response.status_code == 200
        result = response.json()
        assert result["absolute_humidity"] >= 0

    def test_very_small_temperature(self, client):
        """Test with very small temperature value."""
        data = {"temperature": -273.15, "humidity": 50}  # Absolute zero
        response = client.post("/api/calculate", json=data)

        # Should not fail validation but might produce calculation errors
        # At absolute zero, the calculation might fail due to division by zero
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            result = response.json()
            assert result["absolute_humidity"] >= 0

    def test_boundary_humidity_values(self, client):
        """Test boundary values for humidity."""
        # Test 0% humidity
        data = {"temperature": 25.0, "humidity": 0}
        response = client.post("/api/calculate", json=data)
        assert response.status_code == 200

        # Test 100% humidity
        data = {"temperature": 25.0, "humidity": 100}
        response = client.post("/api/calculate", json=data)
        assert response.status_code == 200

    def test_float_humidity_validation(self, client):
        """Test that float humidity values are rejected."""
        data = {"temperature": 25.0, "humidity": 60.7}
        response = client.post("/api/calculate", json=data)

        # FastAPI with Pydantic should reject float values for int fields
        assert response.status_code == 422
        error = response.json()
        assert "detail" in error


if __name__ == "__main__":
    pytest.main([__file__])
