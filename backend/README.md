# MediKiosk Backend

FastAPI service for MediKiosk.

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

## Run
```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs` once running.

## Structure
- `app/api/v1/` — versioned API routes
- `app/core/` — settings and shared exceptions
- `app/db/` — database connection helpers
- `app/models/` — persistence-layer models
- `app/schemas/` — pydantic request/response schemas
- `app/services/` — business logic
