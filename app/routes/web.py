"""
Web routes for the Absolute Humidity Calculator.

This module contains the main web interface route that serves the HTML page
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
            "active_page": "home",
        },
    )


@router.get(
    "/about",
    response_class=HTMLResponse,
    summary="About Page",
    description="Serve the about page with information about the application and calculation methods",
    responses={
        200: {
            "description": "About page",
            "content": {"text/html": {"example": "HTML about page content"}},
        },
    },
)
async def about(request: Request):
    """
    Serve the about page using Jinja2 template.

    This endpoint renders the HTML page with detailed information about:
    - What absolute humidity is
    - The calculation methods and formulas
    - Physical constants used
    - Input limits and validation
    - Technical implementation details

    Args:
        request: FastAPI Request object for template context

    Returns:
        HTMLResponse: Rendered HTML about page
    """
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "title": f"About - {config.APP_NAME}",
            "api_base_url": config.API_PREFIX,
            "app_name": config.APP_NAME,
            "app_version": config.APP_VERSION,
            "app_description": config.APP_DESCRIPTION,
            "active_page": "about",
            "formulas": {
                "magnus": "es = 6.112 * exp((17.67 * T) / (T + 243.5))",
                "absolute_humidity": "AH = (e * 18.016) / (8314.5 * (T + 273.15)) * 1000",
            },
            "constants": {
                "water_molecular_weight": "18.016",
                "universal_gas_constant": "8314.5",
                "magnus_a": "17.67",
                "magnus_b": "243.5",
                "magnus_c": "6.112",
            },
            "limits": {
                "temperature_min": "-273.15",
                "temperature_max": "1000",
                "humidity_min": "0",
                "humidity_max": "100",
            },
        },
    )
