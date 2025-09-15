#!/usr/bin/env python3
"""
Pytest test suite for absolute humidity calculations.
Tests for input validation and error handling.
"""

import pytest

from app.psychro_calculations import (
    calculate_absolute_humidity,
    validate_humidity,
    validate_temperature,
)


class TestInputValidation:
    """Test input validation functions."""

    @pytest.mark.parametrize(
        "temp",
        [20, 20.5, -10, 100, -273.15, 999.9],
    )
    def test_valid_temperatures(self, temp):
        """Test validation of valid temperature values."""
        result = validate_temperature(temp)
        assert isinstance(result, float)
        assert result == float(temp)

    @pytest.mark.parametrize(
        "temp",
        [-274, 1001, float("inf"), float("nan"), float("-inf")],
    )
    def test_invalid_temperatures(self, temp):
        """Test validation of invalid temperature values."""
        with pytest.raises(ValueError):
            validate_temperature(temp)

    @pytest.mark.parametrize(
        "humidity",
        [0, 50, 100],
    )
    def test_valid_humidity(self, humidity):
        """Test validation of valid humidity values."""
        result = validate_humidity(humidity)
        assert isinstance(result, int)
        assert result == int(humidity)

    @pytest.mark.parametrize(
        "humidity",
        [-1, 101, float("inf"), float("nan"), float("-inf")],
    )
    def test_invalid_humidity(self, humidity):
        """Test validation of invalid humidity values."""
        with pytest.raises(ValueError):
            validate_humidity(humidity)

    def test_float_humidity_validation(self):
        """Test that float humidity values are converted to integers."""
        result = validate_humidity(50.5)
        assert result == 50
        assert isinstance(result, int)

    def test_invalid_types(self):
        """Test validation of invalid input types."""
        invalid_inputs = [None, [], {}]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                validate_temperature(invalid_input)
            with pytest.raises(ValueError):
                validate_humidity(invalid_input)

    def test_string_numeric_types(self):
        """Test validation of string numeric types."""
        with pytest.raises(ValueError):
            validate_temperature("20")
        with pytest.raises(ValueError):
            validate_humidity("50")

    def test_boolean_types(self):
        """Test validation of boolean types."""
        # The current validate_temperature implementation accepts booleans as they are subtypes of int
        # Just test that they're converted to floats correctly
        result = validate_temperature(True)
        assert result == 1.0
        assert isinstance(result, float)

        # Same for humidity - booleans are converted to integers
        result = validate_humidity(True)
        assert result == 1
        assert isinstance(result, int)


class TestErrorHandling:
    """Test error handling in calculations."""

    def test_near_absolute_zero(self):
        """Test behavior near absolute zero."""
        with pytest.raises(ValueError):
            calculate_absolute_humidity(-273.16, 50)

    def test_non_finite_temperature(self):
        """Test handling of non-finite temperature values."""
        non_finite = [float("inf"), float("-inf"), float("nan")]
        for value in non_finite:
            with pytest.raises(ValueError):
                calculate_absolute_humidity(value, 50)

    def test_non_finite_humidity(self):
        """Test handling of non-finite humidity values."""
        non_finite = [float("inf"), float("-inf"), float("nan")]
        for value in non_finite:
            with pytest.raises(ValueError):
                calculate_absolute_humidity(20.0, value)  # pyright: ignore

    def test_input_type_errors(self):
        """Test handling of incorrect input types."""
        invalid_inputs = ["string", None, [], {}]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                calculate_absolute_humidity(invalid_input, 50)
            with pytest.raises(ValueError):
                calculate_absolute_humidity(20.0, invalid_input)


if __name__ == "__main__":
    pytest.main([__file__])
