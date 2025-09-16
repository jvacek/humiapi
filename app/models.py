"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field


class HumidityCalculationRequest(BaseModel):
    """Request model for humidity calculation."""

    temperature: float = Field(..., ge=-273.15, le=10000, description="Temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Relative humidity percentage (0-100)")


class HumidityCalculationResponse(BaseModel):
    """Response model for humidity calculation."""

    absolute_humidity: float = Field(..., description="Absolute humidity in g/m³")
    temperature: float = Field(..., description="Input temperature in Celsius")
    humidity: int = Field(..., description="Input relative humidity percentage")
    unit: str = Field(default="g/m³", description="Unit of measurement")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(default="healthy", description="Health status")


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str = Field(..., description="Error message")
