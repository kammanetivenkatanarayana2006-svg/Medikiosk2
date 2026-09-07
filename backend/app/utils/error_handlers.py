from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base application error class."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)

class ValidationError(AppError):
    """Validation error."""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR", 422)

class DatabaseError(AppError):
    """Database operation error."""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, "DATABASE_ERROR", 500)

def format_error_response(
    message: str,
    code: str = "ERROR",
    status_code: int = 500,
    details: Any = None,
) -> Dict[str, Any]:
    """
    Format standard error response.
    """
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details and settings.is_development:
        response["error"]["details"] = details
    return response

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            message=str(exc.detail),
            code="HTTP_ERROR",
            status_code=exc.status_code,
        ),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content=format_error_response(
            message="Request validation failed",
            code="VALIDATION_ERROR",
            status_code=422,
            details=jsonable_encoder(exc.errors()) if settings.is_development else None,
        ),
    )

async def app_error_handler(request: Request, exc: AppError):
    """Handle application errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            message=exc.message,
            code=exc.code,
            status_code=exc.status_code,
        ),
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions."""
    error_id = id(exc)
    logger.error(f"Unhandled exception [ID: {error_id}]: {exc}", exc_info=True)
    
    if settings.is_production:
        # Don't expose internal errors in production
        return JSONResponse(
            status_code=500,
            content=format_error_response(
                message="An unexpected error occurred",
                code="INTERNAL_ERROR",
                status_code=500,
            ),
        )
    else:
        # In development, include more details for debugging
        return JSONResponse(
            status_code=500,
            content=format_error_response(
                message=f"Internal server error: {str(exc)}",
                code="INTERNAL_ERROR",
                status_code=500,
                details={
                    "error_id": error_id,
                    "traceback": traceback.format_exc() if settings.debug else None,
                },
            ),
        )

def register_error_handlers(app: FastAPI):
    """Register all error handlers with the FastAPI app."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)