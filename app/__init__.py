"""
Absolute Humidity Calculator Application Package.

This package contains the modular components of the FastAPI application
for calculating absolute humidity from temperature and relative humidity.

Modules:
    - models: Pydantic models for request/response validation
    - calculations: Core calculation logic
    - config: Application configuration settings
    - routes: API and web route handlers
"""

from .config import config, get_config
from .models import (
    ErrorResponse,
    HealthResponse,
    HumidityCalculationRequest,
    HumidityCalculationResponse,
)
from .psychro_calculations import calculate_absolute_humidity

__version__ = "0.1.0"
__author__ = "Absolute Humidity Calculator Team"
__description__ = "A FastAPI application for calculating absolute humidity"

# Export main components for easy import
__all__ = [
    "calculate_absolute_humidity",
    "config",
    "get_config",
    "HumidityCalculationRequest",
    "HumidityCalculationResponse",
    "HealthResponse",
    "ErrorResponse",
]
