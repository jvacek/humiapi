#!/usr/bin/env python3
"""
Focused pytest test suite for absolute humidity calculations.
Tests for core functionality only.
"""

import pytest

from app.psychro_calculations import calculate_absolute_humidity


class TestCalculation:
    """Test the absolute humidity calculation function."""

    @pytest.mark.parametrize(
        "temp,humidity,expected_range",
        [
            (20.0, 50, (8.0, 9.0)),  # Room temperature
            (30.0, 80, (24.0, 25.0)),  # Hot and humid
            (0.0, 30, (1.0, 2.0)),  # Cold and dry
        ],
    )
    def test_calculation_values(self, temp, humidity, expected_range):
        """Test that calculations return expected values within range."""
        result = calculate_absolute_humidity(temp, humidity)
        min_expected, max_expected = expected_range

        assert min_expected <= result <= max_expected, (
            f"Expected {min_expected}-{max_expected}, got {result} for {temp}°C, {humidity}% RH"
        )


if __name__ == "__main__":
    pytest.main([__file__])
