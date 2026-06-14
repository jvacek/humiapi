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
templates = Jinja2Templates(directory=str(config.TEMPLATES_DIR))

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
    """Serve the main calculator web interface."""
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
    """Serve the about page describing how the calculation works."""
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
            "limits": {
                "temperature_min": "-100",
                "temperature_max": "100",
                "humidity_min": "0",
                "humidity_max": "100",
            },
        },
    )
