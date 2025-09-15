"""
Psychrometric calculations using PsychroLib.

This module provides functions to calculate absolute humidity and other
psychrometric properties using the PsychroLib package, which implements
the formulas from the ASHRAE Handbook of Fundamentals.
"""

import math
from typing import Union

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
        ValueError: If inputs are invalid or calculation fails
        ZeroDivisionError: If temperature approaches absolute zero

    Examples:
        >>> calculate_absolute_humidity(20.0, 50)
        8.64
        >>> calculate_absolute_humidity(25.5, 60)
        14.21
        >>> calculate_absolute_humidity(0.0, 30)
        1.45
    """
    try:
        # Validate inputs
        temperature_celsius = validate_temperature(temperature_celsius)
        relative_humidity_percent = validate_humidity(relative_humidity_percent)

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


def dewpoint_temperature(temperature_celsius: float, relative_humidity_percent: int) -> float:
    """
    Calculate dewpoint temperature given dry bulb temperature and relative humidity.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity as percentage (0-100)

    Returns:
        float: Dewpoint temperature in Celsius, rounded to 2 decimal places
    """
    temperature_celsius = validate_temperature(temperature_celsius)
    relative_humidity_percent = validate_humidity(relative_humidity_percent)

    # Convert relative humidity from percentage to decimal
    rh_decimal = relative_humidity_percent / 100.0

    dewpoint = psychrolib.GetTDewPointFromRelHum(temperature_celsius, rh_decimal)
    return round(dewpoint, 2)


def wetbulb_temperature(
    temperature_celsius: float,
    relative_humidity_percent: int,
    pressure_pa: float = 101325,
) -> float:
    """
    Calculate wet bulb temperature given dry bulb temperature and relative humidity.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity as percentage (0-100)
        pressure_pa (float, optional): Atmospheric pressure in Pa. Defaults to 101325 (standard).

    Returns:
        float: Wet bulb temperature in Celsius, rounded to 2 decimal places
    """
    temperature_celsius = validate_temperature(temperature_celsius)
    relative_humidity_percent = validate_humidity(relative_humidity_percent)

    # Convert relative humidity from percentage to decimal
    rh_decimal = relative_humidity_percent / 100.0

    humidity_ratio = psychrolib.GetHumRatioFromRelHum(temperature_celsius, rh_decimal, pressure_pa)

    wetbulb = psychrolib.GetTWetBulbFromHumRatio(temperature_celsius, humidity_ratio, pressure_pa)

    return round(wetbulb, 2)


def enthalpy(temperature_celsius: float, relative_humidity_percent: int) -> float:
    """
    Calculate specific enthalpy of moist air.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity as percentage (0-100)

    Returns:
        float: Specific enthalpy in kJ/kg dry air, rounded to 2 decimal places
    """
    temperature_celsius = validate_temperature(temperature_celsius)
    relative_humidity_percent = validate_humidity(relative_humidity_percent)

    # Convert relative humidity from percentage to decimal
    rh_decimal = relative_humidity_percent / 100.0

    humidity_ratio = psychrolib.GetHumRatioFromRelHum(temperature_celsius, rh_decimal, 101325)

    # Get enthalpy (J/kg dry air) and convert to kJ/kg
    enthalpy_value = psychrolib.GetMoistAirEnthalpy(temperature_celsius, humidity_ratio) / 1000

    return round(enthalpy_value, 2)


def saturation_vapor_pressure(temperature_celsius: float) -> float:
    """
    Calculate saturation vapor pressure using PsychroLib.

    Args:
        temperature_celsius (float): Temperature in Celsius

    Returns:
        float: Saturation vapor pressure in Pa
    """
    temperature_celsius = validate_temperature(temperature_celsius)
    return psychrolib.GetSatVapPres(temperature_celsius)


def actual_vapor_pressure(temperature_celsius: float, relative_humidity_percent: int) -> float:
    """
    Calculate actual vapor pressure from temperature and relative humidity.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity percentage (0-100)

    Returns:
        float: Actual vapor pressure in Pa
    """
    temperature_celsius = validate_temperature(temperature_celsius)
    relative_humidity_percent = validate_humidity(relative_humidity_percent)

    # Convert relative humidity from percentage to decimal
    rh_decimal = relative_humidity_percent / 100.0

    # Get saturation vapor pressure and multiply by RH
    svp = psychrolib.GetSatVapPres(temperature_celsius)
    return svp * rh_decimal


def validate_temperature(temperature: Union[int, float]) -> float:
    """
    Validate temperature input.

    Args:
        temperature: Temperature value to validate

    Returns:
        float: Validated temperature

    Raises:
        ValueError: If temperature is invalid
    """
    if not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be a number")

    if not math.isfinite(temperature):
        raise ValueError("Temperature must be a finite number")

    # Reasonable bounds check (not absolute zero to 1000°C)
    if temperature < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")

    if temperature > 1000:
        raise ValueError("Temperature too high for accurate calculation")

    return float(temperature)


def validate_humidity(humidity: Union[int, float]) -> int:
    """
    Validate humidity input.

    Args:
        humidity: Humidity percentage to validate

    Returns:
        int: Validated humidity as integer

    Raises:
        ValueError: If humidity is invalid
    """
    if not isinstance(humidity, (int, float)):
        raise ValueError("Humidity must be a number")

    if not math.isfinite(humidity):
        raise ValueError("Humidity must be a finite number")

    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100")

    return int(humidity)
