#!/usr/bin/env python3
"""
Simplified pytest test suite for FastAPI application core functionality.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_api_health_check(self, client):
        """Test /api/health endpoint returns success."""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.json()
        assert data == {"status": "healthy"}


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

        # Check unit is correct
        assert result["unit"] == "g/m³"


class TestHttpMethods:
    """Test HTTP method restrictions."""

    def test_get_not_allowed_on_calculate(self, client):
        """Test that GET is not allowed on calculate endpoint."""
        response = client.get("/api/calculate")
        assert response.status_code == 405  # Method Not Allowed


if __name__ == "__main__":
    pytest.main([__file__])
