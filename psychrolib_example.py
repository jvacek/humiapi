#!/usr/bin/env python3
"""
Example script demonstrating the use of PsychroLib for psychrometric calculations.

This script shows how to use the PsychroLib-based calculations to compute
various psychrometric properties like absolute humidity, dewpoint temperature,
wetbulb temperature, and enthalpy.

Usage:
    python psychrolib_example.py
"""

from app.psychro_calculations import (
    actual_vapor_pressure,
    calculate_absolute_humidity,
    dewpoint_temperature,
    enthalpy,
    saturation_vapor_pressure,
    wetbulb_temperature,
)


def print_separator():
    """Print a separator line for better readability."""
    print("-" * 60)


def compare_conditions(temp, rh, description):
    """
    Calculate and display various psychrometric properties for a given condition.

    Args:
        temp (float): Temperature in Celsius
        rh (int): Relative humidity as percentage (0-100)
        description (str): Description of the condition
    """
    print(f"\n{description} (Temperature: {temp}°C, Relative Humidity: {rh}%)")
    print_separator()

    try:
        abs_humidity = calculate_absolute_humidity(temp, rh)
        dewpoint = dewpoint_temperature(temp, rh)
        wetbulb = wetbulb_temperature(temp, rh)
        enth = enthalpy(temp, rh)
        svp = saturation_vapor_pressure(temp)
        avp = actual_vapor_pressure(temp, rh)

        print(f"Absolute Humidity: {abs_humidity} g/m³")
        print(f"Dewpoint Temperature: {dewpoint}°C")
        print(f"Wetbulb Temperature: {wetbulb}°C")
        print(f"Specific Enthalpy: {enth} kJ/kg")
        print(f"Saturation Vapor Pressure: {svp / 100:.2f} hPa")
        print(f"Actual Vapor Pressure: {avp / 100:.2f} hPa")
    except Exception as e:
        print(f"Error in calculation: {e}")


def main():
    """Main function demonstrating psychrometric calculations."""
    print("\nPSYCHROMETRIC CALCULATOR USING PSYCHROLIB")
    print("=========================================")
    print("Demonstrates calculations of various psychrometric properties")
    print("using the PsychroLib package instead of custom implementation.")

    # Standard room condition
    compare_conditions(20.0, 50, "Standard Room Condition")

    # Hot and humid condition
    compare_conditions(30.0, 80, "Hot and Humid Condition")

    # Cold and dry condition
    compare_conditions(0.0, 30, "Cold and Dry Condition")

    # Desert condition
    compare_conditions(45.0, 10, "Desert Condition")

    # Tropical condition
    compare_conditions(30.0, 90, "Tropical Condition")

    # Indoor heated air condition
    compare_conditions(22.0, 40, "Indoor Heated Air Condition")

    # Try a potential error condition
    print("\nAttempting calculation with extreme values")
    print_separator()
    try:
        result = calculate_absolute_humidity(-300, 50)
        print(f"Result (should not reach here): {result}")
    except ValueError as e:
        print(f"Expected error: {e}")


if __name__ == "__main__":
    main()
