"""
Configuration settings for the Absolute Humidity Calculator application.
"""

from pathlib import Path
from typing import Any, Dict


class Config:
    """Application configuration."""

    # Application metadata
    APP_NAME = "Absolute Humidity Calculator"
    APP_VERSION = "0.2.0"
    APP_DESCRIPTION = "Calculate absolute humidity from temperature and relative humidity."

    # Server settings
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True
    LOG_LEVEL = "info"

    # API / docs URLs
    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    OPENAPI_URL = "/openapi.json"

    # File paths
    BASE_DIR = Path(__file__).parent.parent
    TEMPLATES_DIR = BASE_DIR / "templates"
    STATIC_DIR = BASE_DIR / "static"

    # Response formatting
    DEFAULT_UNIT = "g/m³"

    # CORS
    ALLOW_ORIGINS = ["*"]
    ALLOW_METHODS = ["GET", "POST"]
    ALLOW_HEADERS = ["*"]

    @classmethod
    def get_uvicorn_config(cls) -> Dict[str, Any]:
        """Get configuration for the uvicorn server."""
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "reload": cls.RELOAD,
            "log_level": cls.LOG_LEVEL,
        }

    @classmethod
    def get_fastapi_config(cls) -> Dict[str, Any]:
        """Get configuration for FastAPI app initialization."""
        return {
            "title": cls.APP_NAME,
            "description": cls.APP_DESCRIPTION,
            "version": cls.APP_VERSION,
            "docs_url": cls.DOCS_URL,
            "redoc_url": None,  # ReDoc disabled; Swagger UI at /docs covers the same schema
            "openapi_url": cls.OPENAPI_URL,
        }


config = Config()
