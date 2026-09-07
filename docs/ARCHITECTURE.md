# MediKiosk - Architecture

## System Overview
MediKiosk follows a modern full-stack architecture with clear separation of concerns.

## Frontend Architecture
- **Framework:** React with Vite
- **State Management:** React Hooks (Phase 1)
- **Routing:** React Router
- **Structure:**
  - `components/` - Reusable UI components
  - `pages/` - Page-level components
  - `layouts/` - Layout wrappers
  - `services/` - API service layer
  - `hooks/` - Custom React hooks
  - `utils/` - Utility functions
  - `assets/` - Static assets
  - `styles/` - Global styles
  - `config/` - Configuration files

## Backend Architecture
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn
- **Validation:** Pydantic
- **Structure:**
  - `api/` - API routes and endpoints
  - `core/` - Core configuration and middleware
  - `models/` - Database models
  - `schemas/` - Pydantic schemas
  - `services/` - Business logic
  - `db/` - Database connection and operations
  - `utils/` - Utility functions

## Database Architecture
- **Primary Database:** MongoDB
- **Driver:** Motor (async)
- **Abstraction Layer:** Clean database module with graceful fallback
- **Collections (Planned):** users, patients, doctors, consultations, etc.

## API Layer
- **REST API:** FastAPI-based
- **Documentation:** Auto-generated OpenAPI (Swagger)
- **Versioning:** URL-based (/api/v1)
- **Error Handling:** Centralized with consistent format

## AI Service Layer (Future)
- **Local LLM:** Qwen3 1.7B via Ollama
- **ASR:** Sarvam API
- **TTS:** To be selected
- **OCR:** Dedicated pipeline
- **Isolation:** AI services isolated from core application

## External Integrations (Future)
- Email service
- WhatsApp Business API
- SMS gateway
- Cloud storage for medical reports

## Security Boundary
- Authentication layer (JWT)
- Authorization middleware
- Data encryption at rest
- HTTPS enforcement
- Rate limiting
- Audit logging

## Data Flow (High Level)
# MediKiosk - Architecture

[Previous content preserved...]

## Future System Data Flow (NOT IMPLEMENTED)

The following data flow represents the planned architecture for future phases:

**Note:** This flow is for Phase 3+ implementation. Phase 2 focuses on architecture and governance only.

## Service Boundaries

### Core Services (Phase 3+)
- Authentication Service
- Patient Management Service
- Doctor Management Service
- Consultation Service
- Clinical History Service

### AI Services (Phase 10+)
- ASR Service (Sarvam)
- LLM Service (Ollama/Qwen3)
- TTS Service (Provider TBD)
- OCR Service

### Integration Services (Phase 23+)
- Email Service
- WhatsApp Service
- SMS Service
- PDF Generation Service

### Security Services
- Rate Limiting
- Audit Logging
- Access Control

## Configuration Management

### Environment-Based Configuration
- **Development:** Debug mode, local services, verbose logging
- **Testing:** Minimal logging, test databases
- **Production:** Optimized settings, security enforced

### Configuration Files
- `.env.development` - Development settings
- `.env.testing` - Testing settings
- `.env.production` - Production settings
- `.env.example` - Template for all environments
# MediKiosk - Architecture

[Previous content preserved...]

## Frontend Architecture (Phase 5 Update)

### Route Structure
- `/` → Cinematic Welcome Experience
- `/onboarding` → Patient Onboarding (placeholder for Phase 6)

### Component Architecture

### Welcome Experience Components
- WelcomeBackground: Animated medical grid with particles
- HeartbeatWave: Canvas-based heartbeat waveform
- MediKioskLogo: Animated logo with SVG
- WelcomeHero: Text animations
- AIOrb: Pulsing orb with orbital rings
- WelcomeActions: Primary CTA button
- SkipIntroButton: Accessibility control
- CinematicSequence: Main orchestration component

### TTS Abstraction Boundary
- Future TTS will use voiceService abstraction
- Phase 5: No external TTS integration
- Provider selection deferred to future phase
# MediKiosk - Architecture

[Previous content preserved...]

## Patient Onboarding Flow (Phase 6)

### Route Structure

### Onboarding Components
- PatientTypeSelection: New vs Returning patient
- PatientIdentityForm: Collects basic identity info
- ProfileConfirmation: Review and confirm details
- OnboardingProgress: Visual step indicator
- ReturningPatientPlaceholder: Future auth placeholder

### Temporary State Management
- Session storage for onboarding data
- Cleared after phase completion
- No sensitive data in localStorage
- In-memory state preferred

### Authentication Boundary
- Phase 6: Collect and validate info only
- Future: OTP, email verification, JWT
- No backend authentication yet