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
        },
    )


# About page and health check endpoint removed to simplify web routes
