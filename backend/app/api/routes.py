from fastapi import APIRouter
from app.api.endpoints import health
from app.api.endpoints import auth
from app.api.endpoints import patients
from app.api.endpoints import consultations
from app.api.v1 import router as v1_router
from app.api.endpoints import interviews
from app.api.endpoints import voice
from app.api.endpoints import ai
from app.api.endpoints import clinical_history
from app.api.endpoints import medical_documents
from app.api.endpoints import longitudinal
from app.api.endpoints import follow_up
from app.api.endpoints import ayush

api_router = APIRouter()

api_router.include_router(health.router, tags=["system"])
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(patients.router, tags=["patients"])
api_router.include_router(consultations.router, tags=["consultations"])
api_router.include_router(v1_router, prefix="/v1")
api_router.include_router(interviews.router, tags=["interviews"])
api_router.include_router(voice.router, tags=["voice"])
api_router.include_router(ai.router, tags=["ai"])
api_router.include_router(clinical_history.router, tags=["clinical-history"])
api_router.include_router(medical_documents.router, tags=["medical-documents"])
api_router.include_router(longitudinal.router, tags=["history"])
api_router.include_router(follow_up.router, tags=["follow-up"])
api_router.include_router(ayush.router, tags=["ayush"])
