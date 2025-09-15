import math
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


def calculate_absolute_humidity(
    temperature_celsius: float, relative_humidity_percent: int
) -> float:
    """
    Calculate absolute humidity given temperature and relative humidity.

    Args:
        temperature_celsius (float): Temperature in Celsius
        relative_humidity_percent (int): Relative humidity as percentage (0-100)

    Returns:
        float: Absolute humidity in g/m³
    """
    # Convert relative humidity from percentage to decimal
    rh = relative_humidity_percent / 100.0

    # Calculate saturation vapor pressure using Magnus formula
    # es = 6.112 * exp((17.67 * T) / (T + 243.5))
    # where T is temperature in Celsius and es is in hPa
    saturation_vapor_pressure = 6.112 * math.exp(
        (17.67 * temperature_celsius) / (temperature_celsius + 243.5)
    )

    # Calculate actual vapor pressure
    actual_vapor_pressure = rh * saturation_vapor_pressure

    # Convert to absolute humidity using the ideal gas law
    # Formula: AH = (e * Mw) / (R * T)
    # where:
    # e = actual vapor pressure in Pa (convert from hPa by * 100)
    # Mw = molecular weight of water = 18.016 g/mol
    # R = specific gas constant for water vapor = 461.5 J/(kg·K)
    # T = temperature in Kelvin
    # Result is in kg/m³, multiply by 1000 to get g/m³

    actual_vapor_pressure_pa = actual_vapor_pressure * 100  # Convert hPa to Pa
    temperature_kelvin = temperature_celsius + 273.15

    # AH in kg/m³
    absolute_humidity_kg = (actual_vapor_pressure_pa * 18.016) / (
        8314.5 * temperature_kelvin
    )

    # Convert to g/m³
    absolute_humidity = absolute_humidity_kg * 1000

    return round(absolute_humidity, 2)


# Pydantic models for request/response
class HumidityCalculationRequest(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: int = Field(
        ..., ge=0, le=100, description="Relative humidity percentage (0-100)"
    )


class HumidityCalculationResponse(BaseModel):
    absolute_humidity: float = Field(..., description="Absolute humidity in g/m³")
    temperature: float = Field(..., description="Input temperature in Celsius")
    humidity: int = Field(..., description="Input relative humidity percentage")
    unit: str = Field(default="g/m³", description="Unit of measurement")


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Health status")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


# Create FastAPI app
app = FastAPI(
    title="Absolute Humidity Calculator",
    description="A FastAPI application that calculates absolute humidity from temperature and relative humidity",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Set up static files (if needed in the future)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse, summary="Web Interface")
async def index(request: Request):
    """Serve the main web interface using Jinja2 template."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Absolute Humidity Calculator",
            "api_base_url": "/api",
        },
    )


@app.post(
    "/api/calculate",
    response_model=HumidityCalculationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
    summary="Calculate Absolute Humidity",
    description="Calculate absolute humidity given temperature in Celsius and relative humidity percentage",
)
async def calculate(request: HumidityCalculationRequest):
    """API endpoint to calculate absolute humidity."""
    try:
        # Calculate absolute humidity
        abs_humidity = calculate_absolute_humidity(
            request.temperature, request.humidity
        )

        return HumidityCalculationResponse(
            absolute_humidity=abs_humidity,
            temperature=request.temperature,
            humidity=request.humidity,
            unit="g/m³",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running properly",
)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check (Alternative)",
    description="Alternative health check endpoint for compatibility",
)
async def health_alt():
    """Alternative health check endpoint for compatibility."""
    return HealthResponse(status="healthy")


# Error handlers
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """Handle validation errors with custom response."""
    return {
        "error": "Invalid input parameters. Please check your temperature and humidity values."
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
