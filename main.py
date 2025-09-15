"""
Absolute Humidity Calculator - FastAPI Application

A modern web application for calculating absolute humidity from temperature
and relative humidity inputs. This is the main entry point that creates
and configures the FastAPI application.

Usage:
    python main.py              # Run with default settings
    uvicorn main:app --reload   # Run with uvicorn directly
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.routes import api_router, web_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Initialize FastAPI with configuration
    app = FastAPI(**config.get_fastapi_config())

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=config.ALLOW_METHODS,
        allow_headers=config.ALLOW_HEADERS,
    )

    # Mount static files if directory exists
    if config.STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

    # Include routers
    app.include_router(web_router)
    app.include_router(api_router)

    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        """Application startup event handler."""
        print(f"🌡️  {config.APP_NAME} v{config.APP_VERSION}")
        print(f"🚀 Server starting on http://{config.HOST}:{config.PORT}")
        print(f"📖 API docs available at http://{config.HOST}:{config.PORT}{config.DOCS_URL}")
        print(f"📋 Alternative docs at http://{config.HOST}:{config.PORT}{config.REDOC_URL}")

    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Application shutdown event handler."""
        print("🛑 Server shutting down...")

    # Add exception handlers
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions with appropriate HTTP responses."""
        return JSONResponse(status_code=400, content={"error": f"Invalid input: {str(exc)}"})

    @app.exception_handler(ZeroDivisionError)
    async def zero_division_error_handler(request: Request, exc: ZeroDivisionError):
        """Handle ZeroDivisionError exceptions."""
        return JSONResponse(
            status_code=400,
            content={"error": "Temperature too low for calculation (division by zero)"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        return JSONResponse(status_code=500, content={"error": f"Internal server error: {str(exc)}"})

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    # Run the server when script is executed directly
    uvicorn.run("main:app", **config.get_uvicorn_config())
