"""
Psychrometric calculations using PsychroLib.

This module provides a function to calculate absolute humidity
using the PsychroLib package, which implements the formulas from
the ASHRAE Handbook of Fundamentals.
"""


import psychrolib

# Set unit system to SI (metric)
psychrolib.SetUnitSystem(psychrolib.SI)


def calculate_absolute_humidity(temperature_celsius: float, relative_humidity_percent: int) -> float:
    """
    Calculate absolute humidity given temperature and relative humidity.

    Uses PsychroLib to calculate humidity ratio and then converts to absolute humidity.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity as percentage (0-100)

    Returns:
        float: Absolute humidity in g/m³, rounded to 2 decimal places

    Raises:
        ValueError: If calculation fails
        ZeroDivisionError: If temperature approaches absolute zero
    """
    try:
        # Convert relative humidity from percentage to decimal
        rh_decimal = relative_humidity_percent / 100.0

        # Get humidity ratio (kg water / kg dry air)
        humidity_ratio = psychrolib.GetHumRatioFromRelHum(
            temperature_celsius,
            rh_decimal,
            101325,  # Standard atmospheric pressure in Pa
        )

        # Convert humidity ratio to absolute humidity (g/m³)
        absolute_humidity = (
            psychrolib.GetMoistAirDensity(
                temperature_celsius,
                humidity_ratio,
                101325,  # Standard atmospheric pressure in Pa
            )
            * humidity_ratio
            * 1000
        )  # Convert from kg/m³ to g/m³

        return round(absolute_humidity, 2)

    except (ValueError, ZeroDivisionError) as e:
        raise e
    except Exception as e:
        raise ValueError(f"Calculation failed: {str(e)}")


# Validation functions removed - we rely on Pydantic for input validation
