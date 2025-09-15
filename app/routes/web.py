"""
Web routes for the Absolute Humidity Calculator.

This module contains the web interface routes that serve HTML pages
using Jinja2 templates.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..config import config

# Initialize Jinja2 templates
templates = Jinja2Templates(**config.get_template_config())

# Create web router
router = APIRouter(
    tags=["web"],
    responses={
        404: {"description": "Page not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Web Interface",
    description="Serve the main web interface for calculating absolute humidity",
    responses={
        200: {
            "description": "Main web interface",
            "content": {"text/html": {"example": "HTML page content"}},
        },
    },
)
async def index(request: Request):
    """
    Serve the main web interface using Jinja2 template.

    This endpoint renders the main HTML page with a responsive form
    for calculating absolute humidity. The page includes:
    - Temperature input (Celsius)
    - Humidity input (percentage)
    - Interactive examples
    - Real-time calculation via JavaScript

    Args:
        request: FastAPI Request object for template context

    Returns:
        HTMLResponse: Rendered HTML page
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": config.APP_NAME,
            "api_base_url": config.API_PREFIX,
            "app_version": config.APP_VERSION,
            "app_description": config.APP_DESCRIPTION,
        },
    )


@router.get(
    "/about",
    response_class=HTMLResponse,
    summary="About Page",
    description="Information about the absolute humidity calculator",
    responses={
        200: {
            "description": "About page",
            "content": {"text/html": {"example": "HTML about page content"}},
        },
    },
)
async def about(request: Request):
    """
    Serve an about page with information about the calculator.

    This page could include:
    - Information about absolute humidity
    - Calculation methods and formulas
    - Usage examples
    - Technical details

    Args:
        request: FastAPI Request object for template context

    Returns:
        HTMLResponse: Rendered about page
    """
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "title": f"About - {config.APP_NAME}",
            "app_name": config.APP_NAME,
            "app_version": config.APP_VERSION,
            "formulas": {
                "magnus": f"es = {config.MAGNUS_C} * exp(({config.MAGNUS_A} * T) / (T + {config.MAGNUS_B}))",
                "absolute_humidity": f"AH = (e * {config.WATER_MOLECULAR_WEIGHT}) / ({config.UNIVERSAL_GAS_CONSTANT} * (T + 273.15)) * 1000",
            },
            "constants": {
                "water_molecular_weight": config.WATER_MOLECULAR_WEIGHT,
                "universal_gas_constant": config.UNIVERSAL_GAS_CONSTANT,
                "magnus_a": config.MAGNUS_A,
                "magnus_b": config.MAGNUS_B,
                "magnus_c": config.MAGNUS_C,
            },
            "limits": {
                "temperature_min": config.MIN_TEMPERATURE,
                "temperature_max": config.MAX_TEMPERATURE,
                "humidity_min": config.MIN_HUMIDITY,
                "humidity_max": config.MAX_HUMIDITY,
            },
        },
    )


# Health check endpoint for web interface (alternative path)
@router.get(
    "/health",
    summary="Web Health Check",
    description="Alternative health check endpoint for compatibility",
    responses={
        200: {
            "description": "Health status",
            "content": {"application/json": {"example": {"status": "healthy"}}},
        },
    },
)
async def health_check_alt():
    """
    Alternative health check endpoint for compatibility.

    This provides the same health check functionality as the API endpoint
    but at the root level for backward compatibility.

    Returns:
        dict: Health status response
    """
    return config.HEALTH_CHECK_RESPONSE
