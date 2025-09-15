"""
Routes package for the Absolute Humidity Calculator.

This package contains all the route handlers for the FastAPI application,
organized into separate modules for API and web routes.

Modules:
    - api: REST API endpoints for calculations and health checks
    - web: Web interface routes serving HTML templates
"""

from .api import router as api_router
from .web import router as web_router

__all__ = ["api_router", "web_router"]
