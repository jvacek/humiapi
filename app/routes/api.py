"""
API routes for the Absolute Humidity Calculator.

This module contains the core API endpoint for calculating absolute humidity.
"""

from fastapi import APIRouter

from ..config import config
from ..models import (
    ErrorResponse,
    HealthResponse,
    HumidityCalculationRequest,
    HumidityCalculationResponse,
)
from ..psychro_calculations import calculate_absolute_humidity

# Create API router
router = APIRouter(
    prefix=config.API_PREFIX,
    tags=["api"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)


@router.post(
    "/calculate",
    response_model=HumidityCalculationResponse,
    summary="Calculate Absolute Humidity",
    description=(
        "Calculate absolute humidity given temperature in Celsius and "
        "relative humidity percentage. Uses PsychroLib for accurate "
        "psychrometric calculations based on ASHRAE standards."
    ),
    responses={
        200: {
            "description": "Successful calculation",
            "model": HumidityCalculationResponse,
        },
        422: {
            "description": "Validation error - invalid input parameters",
            "model": ErrorResponse,
        },
        500: {
            "description": "Calculation error",
            "model": ErrorResponse,
        },
    },
)
async def calculate_humidity(request: HumidityCalculationRequest):
    """
    Calculate absolute humidity from temperature and relative humidity.

    Uses PsychroLib's psychrometric functions, which implement the ASHRAE
    Handbook of Fundamentals formulas. A failed calculation raises ValueError,
    which the app translates into a 400 response.
    """
    abs_humidity = calculate_absolute_humidity(request.temperature, request.humidity)

    return HumidityCalculationResponse(
        absolute_humidity=abs_humidity,
        temperature=request.temperature,
        humidity=request.humidity,
        unit=config.DEFAULT_UNIT,
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API Health Check",
    description="Check if the API is running and healthy",
    responses={
        200: {
            "description": "API is healthy",
            "model": HealthResponse,
        },
    },
)
async def health_check():
    """
    Health check endpoint for API monitoring.

    Returns a simple status response to indicate the API is running
    and responding to requests.

    Returns:
        HealthResponse: Status indicating API health
    """
    return HealthResponse(status="healthy")


# Info endpoint removed to simplify API
