"""
Absolute Humidity Calculator - FastAPI Application

A web application for calculating absolute humidity from temperature
and relative humidity inputs. This is the main entry point that creates
and configures the FastAPI application.

Usage:
    python main.py              # Run with default settings
    uvicorn main:app --reload   # Run with uvicorn directly
"""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.routes import api_router, web_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log startup/shutdown around the application lifetime."""
    logger.info("%s v%s starting on http://%s:%s", config.APP_NAME, config.APP_VERSION, config.HOST, config.PORT)
    yield
    logger.info("Server shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(lifespan=lifespan, **config.get_fastapi_config())

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS,
        allow_methods=config.ALLOW_METHODS,
        allow_headers=config.ALLOW_HEADERS,
    )

    if config.STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

    app.include_router(web_router)
    app.include_router(api_router)

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Return invalid calculation inputs as 400 responses."""
        return JSONResponse(status_code=400, content={"error": f"Invalid input: {exc}"})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Log unexpected errors and return a generic 500 response."""
        logger.exception("Unhandled error processing %s", request.url.path)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", **config.get_uvicorn_config())
