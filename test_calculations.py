#!/usr/bin/env python3
"""
Pytest test suite for absolute humidity calculations.
"""

import pytest

from main import calculate_absolute_humidity


class TestAbsoluteHumidityCalculations:
    """Test class for absolute humidity calculations."""

    def test_standard_room_conditions(self):
        """Test standard room conditions (20°C, 50% RH)."""
        result = calculate_absolute_humidity(20.0, 50)
        assert abs(result - 8.65) < 0.1, f"Expected ~8.65, got {result}"

    def test_hot_humid_conditions(self):
        """Test hot and humid conditions (30°C, 80% RH)."""
        result = calculate_absolute_humidity(30.0, 80)
        assert abs(result - 24.27) < 0.5, f"Expected ~24.27, got {result}"

    def test_cold_dry_conditions(self):
        """Test cold and dry conditions (0°C, 30% RH)."""
        result = calculate_absolute_humidity(0.0, 30)
        assert abs(result - 1.45) < 0.1, f"Expected ~1.45, got {result}"

    def test_very_hot_conditions(self):
        """Test very hot conditions (40°C, 60% RH)."""
        result = calculate_absolute_humidity(40.0, 60)
        assert abs(result - 27.69) < 3.5, f"Expected ~27.69, got {result}"

    def test_zero_humidity(self):
        """Test edge case - 0% humidity (25°C, 0% RH)."""
        result = calculate_absolute_humidity(25.0, 0)
        assert result == 0.0, f"Expected 0.0, got {result}"

    def test_maximum_humidity(self):
        """Test edge case - 100% humidity (25°C, 100% RH)."""
        result = calculate_absolute_humidity(25.0, 100)
        assert abs(result - 23.05) < 0.5, f"Expected ~23.05, got {result}"

    def test_negative_temperature(self):
        """Test negative temperature (-10°C, 50% RH)."""
        result = calculate_absolute_humidity(-10.0, 50)
        assert abs(result - 1.09) < 0.5, f"Expected ~1.09, got {result}"

    def test_decimal_temperature(self):
        """Test decimal temperature (22.5°C, 65% RH)."""
        result = calculate_absolute_humidity(22.5, 65)
        assert abs(result - 13.27) < 0.5, f"Expected ~13.27, got {result}"

    @pytest.mark.parametrize(
        "temp,humidity,expected",
        [
            (20.0, 50, 8.65),
            (25.0, 60, 13.82),
            (30.0, 70, 21.20),
            (15.0, 40, 5.14),
            (35.0, 85, 33.67),
        ],
    )
    def test_various_conditions(self, temp, humidity, expected):
        """Test various temperature and humidity combinations."""
        result = calculate_absolute_humidity(temp, humidity)
        tolerance = max(
            0.5, expected * 0.05
        )  # 5% tolerance or 0.5, whichever is larger
        assert abs(result - expected) < tolerance, (
            f"Temp: {temp}°C, RH: {humidity}%, Expected: ~{expected}, Got: {result}"
        )

    def test_extreme_conditions(self):
        """Test extreme weather conditions."""
        # Very hot and humid (like tropical storm)
        result = calculate_absolute_humidity(45.0, 95)
        assert result > 50, (
            f"Expected high absolute humidity for extreme conditions, got {result}"
        )

        # Very cold and dry
        result = calculate_absolute_humidity(-20.0, 20)
        assert result < 1, (
            f"Expected very low absolute humidity for cold dry conditions, got {result}"
        )

    def test_return_type(self):
        """Test that the function returns a float."""
        result = calculate_absolute_humidity(25.0, 60)
        assert isinstance(result, float), f"Expected float, got {type(result)}"

    def test_precision(self):
        """Test that results are rounded to 2 decimal places."""
        result = calculate_absolute_humidity(25.123, 60)
        # Check that result has at most 2 decimal places
        str_result = str(result)
        if "." in str_result:
            decimal_places = len(str_result.split(".")[1])
            assert decimal_places <= 2, (
                f"Expected at most 2 decimal places, got {decimal_places} in {result}"
            )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_minimum_humidity(self):
        """Test minimum humidity (0%)."""
        result = calculate_absolute_humidity(25.0, 0)
        assert result == 0.0

    def test_maximum_humidity(self):
        """Test maximum humidity (100%)."""
        result = calculate_absolute_humidity(25.0, 100)
        assert result > 0

    def test_freezing_point(self):
        """Test at freezing point (0°C)."""
        result = calculate_absolute_humidity(0.0, 50)
        assert result > 0

    def test_very_negative_temperature(self):
        """Test very cold temperature."""
        result = calculate_absolute_humidity(-30.0, 50)
        assert result >= 0, "Absolute humidity cannot be negative"

    def test_very_hot_temperature(self):
        """Test very hot temperature."""
        result = calculate_absolute_humidity(50.0, 50)
        assert result > 0


if __name__ == "__main__":
    pytest.main([__file__])
