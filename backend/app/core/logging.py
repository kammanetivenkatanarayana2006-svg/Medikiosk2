import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os
import sys
from typing import Dict, Any
from app.core.config import settings

LOG_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "format": '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "default",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "detailed",
            "filename": settings.LOG_FILE,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "logs/error.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8",
        },
    },
    "root": {
        "level": settings.LOG_LEVEL,
        "handlers": ["console", "file", "error_file"] if not settings.is_testing else ["console"],
    },
    "loggers": {
        "app": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console", "file"] if not settings.is_testing else ["console"],
            "propagate": False,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

def setup_logging():
    """
    Configure application logging based on environment.
    """
    # Ensure logs directory exists
    if not settings.is_testing:
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    logging.config.dictConfig(LOG_CONFIG)
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured for environment: {settings.APP_ENV}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the app prefix.
    """
    return logging.getLogger(f"app.{name}")