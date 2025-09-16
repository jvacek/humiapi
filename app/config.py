"""
Configuration settings for the Absolute Humidity Calculator application.

This module contains essential configuration constants and settings used
throughout the application.
"""

from pathlib import Path
from typing import Any, Dict


class Config:
    """Main configuration class for the application."""

    # Application metadata
    APP_NAME = "Absolute Humidity Calculator"
    APP_VERSION = "0.1.0"
    APP_DESCRIPTION = (
        "A FastAPI application that calculates absolute humidity from temperature and relative humidity inputs"
    )

    # Server settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    RELOAD = True
    LOG_LEVEL = "info"

    # API settings
    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    OPENAPI_URL = "/openapi.json"

    # File paths
    BASE_DIR = Path(__file__).parent.parent
    TEMPLATES_DIR = BASE_DIR / "templates"
    STATIC_DIR = BASE_DIR / "static"

    # Template settings
    TEMPLATE_AUTO_RELOAD = True

    # Calculation constants - not needed as we use PsychroLib

    # Validation limits
    MIN_TEMPERATURE = -273.15  # Absolute zero in Celsius
    MAX_TEMPERATURE = 1000.0  # Maximum reasonable temperature for calculation
    MIN_HUMIDITY = 0  # Minimum relative humidity percentage
    MAX_HUMIDITY = 100  # Maximum relative humidity percentage

    # Response formatting
    DECIMAL_PLACES = 2
    DEFAULT_UNIT = "g/m³"

    # CORS settings (if needed in the future)
    ALLOW_ORIGINS = ["*"]
    ALLOW_METHODS = ["GET", "POST"]
    ALLOW_HEADERS = ["*"]

    # Health check settings
    HEALTH_CHECK_RESPONSE = {"status": "healthy"}

    @classmethod
    def get_uvicorn_config(cls) -> Dict[str, Any]:
        """Get configuration for uvicorn server."""
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
            "redoc_url": cls.REDOC_URL,
            "openapi_url": cls.OPENAPI_URL,
        }

    @classmethod
    def get_template_config(cls) -> Dict[str, Any]:
        """Get configuration for Jinja2 templates."""
        return {
            "directory": str(cls.TEMPLATES_DIR),
            "auto_reload": cls.TEMPLATE_AUTO_RELOAD,
        }


class DevelopmentConfig(Config):
    """Configuration for development environment."""

    DEBUG = True
    RELOAD = True
    LOG_LEVEL = "debug"


class ProductionConfig(Config):
    """Configuration for production environment."""

    DEBUG = False
    RELOAD = False
    LOG_LEVEL = "warning"
    TEMPLATE_AUTO_RELOAD = False

    # More restrictive CORS in production
    ALLOW_ORIGINS = ["https://yourdomain.com"]


class TestingConfig(Config):
    """Configuration for testing environment."""

    DEBUG = True
    RELOAD = False
    LOG_LEVEL = "error"

    # Use different port for testing
    PORT = 8001


# Default configuration
config = Config()

# Configuration mapping for different environments
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env: str = "development") -> Config:
    """
    Get configuration based on environment.

    Args:
        env: Environment name (development, production, testing)

    Returns:
        Config: Configuration instance for the specified environment
    """
    config_class = CONFIG_MAP.get(env, Config)
    return config_class()
