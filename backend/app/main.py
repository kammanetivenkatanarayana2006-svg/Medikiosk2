from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uuid
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import api_router
from app.db.connection import mongo_connection
from app.db.repositories.user_repository import user_repository
from app.utils.error_handlers import register_error_handlers
from app.db.repositories.patient_repository import patient_repository
from app.db.repositories.otp_repository import otp_repository
from app.db.repositories.verification_token_repository import verification_token_repository
from app.db.repositories.consultation_repository import consultation_repository
from app.db.repositories.interview_repository import interview_repository
from app.db.repositories.clinical_extraction_repository import clinical_extraction_repository
from app.db.repositories.medical_document_repository import medical_document_repository
from app.db.repositories.follow_up_repository import follow_up_repository
from app.db.repositories.ayush_repository import ayush_repository

# In lifespan:
# In lifespan:
# In lifespan:
# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Connect to database
    await mongo_connection.connect()
    
    if mongo_connection.is_connected:
        # Create indexes
        await user_repository.create_indexes()
        await patient_repository.create_indexes()
        await otp_repository.create_indexes()
        await verification_token_repository.create_indexes()
        await consultation_repository.create_indexes()
        await interview_repository.create_indexes()
        await clinical_extraction_repository.create_indexes()
        await medical_document_repository.create_indexes()
        await follow_up_repository.create_indexes()
        await ayush_repository.create_indexes()
        logger.info("Database indexes created")
    
    yield
    
    # Shutdown
    await mongo_connection.disconnect()
    logger.info(f"Shutting down {settings.APP_NAME}")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Clinical Intake & Clinical History Software Platform",
    docs_url="/api/docs" if settings.is_development else None,
    lifespan=lifespan,
)

# Middleware and routes...
# Add request ID middleware
@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handlers
register_error_handlers(app)

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/api/docs" if settings.is_development else None,
        "health": "/api/health",
    }