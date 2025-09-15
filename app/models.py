"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field


class HumidityCalculationRequest(BaseModel):
    """Request model for humidity calculation."""

    temperature: float = Field(..., description="Temperature in Celsius", example=25.5)
    humidity: int = Field(
        ...,
        ge=0,
        le=100,
        description="Relative humidity percentage (0-100)",
        example=60,
    )

    class Config:
        json_schema_extra = {"example": {"temperature": 25.5, "humidity": 60}}


class HumidityCalculationResponse(BaseModel):
    """Response model for humidity calculation."""

    absolute_humidity: float = Field(..., description="Absolute humidity in g/m³", example=14.21)
    temperature: float = Field(..., description="Input temperature in Celsius", example=25.5)
    humidity: int = Field(..., description="Input relative humidity percentage", example=60)
    unit: str = Field(default="g/m³", description="Unit of measurement", example="g/m³")

    class Config:
        json_schema_extra = {
            "example": {
                "absolute_humidity": 14.21,
                "temperature": 25.5,
                "humidity": 60,
                "unit": "g/m³",
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(default="healthy", description="Health status", example="healthy")

    class Config:
        json_schema_extra = {"example": {"status": "healthy"}}


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str = Field(..., description="Error message", example="Invalid input parameters")

    class Config:
        json_schema_extra = {
            "example": {"error": "Invalid input parameters. Please check your temperature and humidity values."}
        }
