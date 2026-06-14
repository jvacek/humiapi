"""
Absolute Humidity Calculator application package.

Modules:
    - models: Pydantic models for request/response validation
    - psychro_calculations: PsychroLib-based calculation logic
    - config: Application configuration settings
    - routes: API and web route handlers
"""

from .config import config
from .models import (
    ErrorResponse,
    HealthResponse,
    HumidityCalculationRequest,
    HumidityCalculationResponse,
)
from .psychro_calculations import calculate_absolute_humidity

__version__ = "0.1.0"

__all__ = [
    "calculate_absolute_humidity",
    "config",
    "HumidityCalculationRequest",
    "HumidityCalculationResponse",
    "HealthResponse",
    "ErrorResponse",
]
