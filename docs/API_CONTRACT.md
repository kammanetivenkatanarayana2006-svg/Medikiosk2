# MediKiosk - API Contract

## Current Endpoints (Phase 1)

### Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "ok",
  "service": "MediKiosk Backend",
  "version": "0.1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "database": "not_configured"
}
# MediKiosk - API Contract

[Previous content preserved...]

## Authentication Endpoints (Phase 7)

### Register
**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "password": "Secure@123"
}