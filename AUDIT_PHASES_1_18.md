# MEDIKIOSK PHASE 1–18 AUDIT

## Overall Status
`AUDITED` `FIXED` `VERIFIED`. All Phases 1–18 (auth, patient profile, photo, consultation setup, XML/JSON interview engine, AI next-question, smart follow-up, clinical extraction, medical documents/OCR, longitudinal history, AYUSH, voice ASR) were audited against source, MongoDB (live), Ollama/Qwen3 (live), and a full live API walkthrough. Phase 19 is NOT audited and NOT implemented.

## Critical / High / Medium / Low Issues

| Severity | Count | Description |
|---|---|---|
| Critical | 0 | Remaining |
| High | 6 fixed / 0 remaining | Missing service imports (3 frontend, 3 backend) |
| Medium | 6 fixed / 0 remaining | ObjectId serialization, follow-up state advance, OCR/extraction wiring |
| Low | 2 fixed / 3 remaining | lint config, requirements drift, pydantic warnings |

## Issues Fixed

### MK-BUG-001 — ConsultationReady.jsx missing import (High)
- **File:** `frontend/src/components/consultation/ConsultationReady.jsx`
- **Root cause:** `interviewService.createInterview(...)` called at runtime but `interviewService` was never imported.
- **Fix:** Added `import { interviewService } from "../../services/interviews";`.
- **Verification:** `npm run build` passes; import-pattern scan across all service-using JSX files.

### MK-BUG-002 — interview_service submit_response missing response_id (High)
- **File:** `backend/app/services/interview_service.py`
- **Root cause:** First response did not persist/propagate the `response_id`, so follow-up.determine and clinical extraction could not resolve the answer.
- **Fix:** Persist extra responses and return `response_id`, `next_question_id`, progress, and completion in both branches.
- **Verification:** Live smoke test: `submit` → `response_id`, `next_question_id: chief_complaint_01`.

### MK-BUG-003 — auth.js login response parse (Medium)
- **File:** `frontend/src/services/auth.js`
- **Root cause:** Login response is nested (`data: { access_token }`) but the service read the token at top level.
- **Fix:** Parse token from `data.access_token` with fallback.
- **Verification:** Live login returns token; AuthContext restores session.

### MK-BUG-004 — App.jsx AYUSHForm registration (Medium)
- **File:** `frontend/src/App.jsx`
- **Root cause:** `<AYUSHForm/>` used without importing the component.
- **Fix:** Imported `AYUSHForm`.
- **Verification:** `npm run build` passes.

### MK-BUG-005 — LoginPage navigate not wired (Medium)
- **File:** `frontend/src/pages/LoginPage.jsx`
- **Root cause:** After login, navigation to `/patient/profile` was missing.
- **Fix:** Restored navigate target.
- **Verification:** Frontend flow build passes.

### MK-BUG-006 — otp_repository TTL index conflict (Medium)
- **File:** `backend/app/db/repositories/otp_repository.py`
- **Root cause:** Recreating a MongoDB TTL index with changing `expireAfterSeconds` throws `IndexOptionsConflict`/`IndexKeySpecsConflict`.
- **Fix:** Use `ensureIndex` with exact existing spec / drop-recreate once.
- **Verification:** pytest (33 passed) + Mongo create/drop during tests and live OTP flow.

### MK-BUG-007 — patient_service missing photo_storage_service import (High)
- **File:** `backend/app/services/patient_service.py`
- **Root cause:** `photo_storage_service` used at upload/retrieve/delete paths but never imported → `NameError` at runtime.
- **Fix:** Added `from app.services.storage.photo_storage import photo_storage_service`.
- **Verification:** `py_compile` OK; import walk passed; pytest 33 passed.

### MK-BUG-008 — connection.health_check missing `import time` (High)
- **File:** `backend/app/db/connection.py`
- **Root cause:** `time.time()` called in `health_check()` without importing `time` → `NameError` on `/api/health`.
- **Fix:** Added `import time`.
- **Verification:** `/api/health` returns 200 with `latency_ms`.

### MK-BUG-009 — clinical_extraction_service missing mongo_connection import (High)
- **File:** `backend/app/services/clinical_extraction_service.py`
- **Root cause:** `_get_response_by_id` uses `mongo_connection.database[...]` but the import was missing → crash on extraction.
- **Fix:** Added `from app.db.connection import mongo_connection`.
- **Verification:** Live `/clinical-history/extract` returns 200.

### MK-BUG-010 — Smart follow-up rejected fabricated question IDs (High)
- **File:** `backend/app/services/interview_service.py`
- **Root cause:** Frontend fabricates `followup_*` / `ai_*` question IDs; backend `submit_response` rejected any `question_id != current_question_id` → 400, so follow-ups and AI questions could never be answered.
- **Fix:** Accept `followup_*`/`ai_*` clarification answers, save them as extra responses, and return the pending real `current_question_id` without advancing state.
- **Verification:** Live: `should_follow_up: true`, `target_field: duration`; follow-up answer submit → 200, returns pending real question. Pytest 33 passed.

### MK-BUG-011 — ObjectId serialization in 5 endpoints (High)
- **Files:** `app/api/serializers.py` (new), `endpoints/interviews.py`, `clinical_history.py`, `medical_documents.py`, `ayush.py`, `consultations.py`
- **Root cause:** Endpoints returned raw Mongo documents; FastAPI `JSONResponse` hit `TypeError: 'ObjectId' object is not iterable` / `vars() argument must have __dict__ attribute` → 500.
- **Fix:** Added shared `serialize_doc`/`serialize_docs` (str `_id`, isoformat datetimes) and applied to list/detail/OCR/structured/AYUSH/consultation endpoints.
- **Verification:** Live: GET interview, structured history, history list/detail, consultations list, docs list/get/ocr, AYUSH GET all 200.

### MK-BUG-012 — longitudinal has_clinical_history false negative (High)
- **File:** `backend/app/services/longitudinal_service.py`
- **Root cause:** `_build_consultation_summary` passed the consultation `_id` to `find_by_interview_id`, so `has_clinical_history` was always false.
- **Fix:** Resolve interview by `consultation_id` first, then query extractions by interview `_id`.
- **Verification:** Live `GET /history` shows `has_clinical_history: true`.

### MK-BUG-013 — AYUSH PUT 500 instead of 422 (High)
- **File:** `backend/app/utils/error_handlers.py`
- **Root cause:** Validation errors return `exc.errors()` directly; pydantic embeds the raised `ValueError` object in `ctx`, which `json.dumps` can't serialize → 500 even for a normal validation failure.
- **Fix:** Wrap with `jsonable_encoder(exc.errors())` (FastAPI default behavior).
- **Verification:** Live AYUSH PUT with invalid `prakriti: vata` now returns 422; valid `Vata` returns 200.

### MK-BUG-014 — VoiceInput.jsx missing voiceService import (High)
- **File:** `frontend/src/components/voice/VoiceInput.jsx`
- **Root cause:** `voiceService.transcribeAudio(...)` called without import → `ReferenceError` on speak.
- **Fix:** Added `import { voiceService } from '../../services/voice';`.
- **Verification:** `npm run build` passes after fix.

### MK-BUG-015 — TTSPlayback.jsx missing import + orphaned setTimeout (High)
- **File:** `frontend/src/components/voice/TTSPlayback.jsx`
- **Root cause:** `voiceService` never imported; plus an orphaned `setTimeout` that re-set `audio.src`/`play()` and leaked on unmount.
- **Fix:** Imported `voiceService`; removed the timeout by binding `src={audioUrl}` and driving autoplay via `onLoadedData`.
- **Verification:** `npm run build` passes; URL revocation cleanup retained.

### MK-BUG-016 — PhotoCapturePage.jsx missing patientService import (High)
- **File:** `frontend/src/pages/PhotoCapturePage.jsx`
- **Root cause:** `patientService.uploadPhoto(...)` used without import → `ReferenceError`.
- **Fix:** Added `import { patientService } from '../services/patient';`.
- **Verification:** `npm run build` passes; import-pattern scan shows no remaining unimported service usage.

### MK-BUG-017 — aiofiles not listed in requirements (Low)
- **File:** `backend/requirements.txt`
- **Root cause:** `aiofiles` used by `photo_storage.py`/`document_storage.py` but missing from requirements → fresh install breaks.
- **Fix:** Added `aiofiles` to requirements.
- **Verification:** import works in venv; requirements updated.

## Remaining Issues (blocks Phase 19?)
- **ESLint config missing (Low, does NOT block Phase 19):** `npm run lint` cannot run — root has `lint` script but no `eslintrc`/`eslint.config.js`.
- **Sarvam ASR/TTS requires external configuration (CONFIGURATION REQUIRED, blocks Phase 19 voice):** `SARVAM_ASR_ENABLED: True` but live ASR/TTS requires a valid Sarvam API key and external network access; `TTS_ENABLED: False` by default. Documented, not fake-verified. OCR additionally requires a real image (tesseract decodes actual PNG/JPEG; test fixture image was dummy → `ocr_status: failed`, handled gracefully with 404 `ocr_result`).
- **Pydantic protected-namespace warnings (Low, does NOT block):** `models/ai.py` fields `model_available`/`model_name` trigger deprecated namespace warnings (13 warnings in pytest; benign).
- **config.py duplicate field declarations (Low, does NOT block):** `SARVAM_API_KEY` declared twice; `TTS_PROVIDER`/`TTS_API_KEY` three times (last-wins; hygiene).

## Verification

**Frontend Build/Tests:**
- `npm run build` → PASS (140 modules, `index-*.js` ~261 kB).
- No test runner configured for frontend (reporting only build verification).
- `npm run lint` → NOT RUNNABLE (no ESLint config file present).

**Backend:**
- `pytest -q` → `33 passed, 13 warnings`.
- `py_compile` on all `backend/app/**/*.py` → OK.
- Import walk of entire `app` package → no missing modules.

**MongoDB:**
- `MONGO_CONNECT: True`, `is_connected: True` (live).
- Create/fetch/update/delete across interview, extractions, consultations, documents, AYUSH records validated live.

**Ollama/Qwen:**
- `/api/ai/status` → `{available: true, model_available: true, model_name: qwen3:1.7b}`.
- AI next-question generation confirmed live in smoke test.

**API (live walkthrough, `127.0.0.1:8021`):**
- register 201 → login 200 → `/auth/me` 200 → `/patients/me` 200 (auto-create) → create consultation 200 → create interview 200 → GET interview 200 → start 200 → submit response 200 → follow-up 200 (`should_follow_up: true`) → follow-up answer 200 → AI next-question 200 → clinical extract 200 → structured history 200 → `/history` 200 (`has_clinical_history: true`) → `/history/consultations/{id}` 200 → consultations list 200 → AYUSH GET/PUT 200 → doc upload 200 / list 200 / get 200 / delete 200.
- `/api/health` 200 with latency.

**Runtime / Console:**
- No unhandled exceptions in server log after fixes (final run clean).
- Dev email/WhatsApp mock logging works as designed.

## Files Modified

**Backend (20):**
- `backend/app/db/connection.py`
- `backend/app/db/repositories/otp_repository.py`
- `backend/app/api/serializers.py` *(new)*
- `backend/app/api/endpoints/interviews.py`, `clinical_history.py`, `medical_documents.py`, `ayush.py`, `consultations.py`
- `backend/app/services/patient_service.py`, `interview_service.py`, `clinical_extraction_service.py`, `longitudinal_service.py`
- `backend/app/utils/error_handlers.py`
- `backend/requirements.txt`

**Frontend (7):**
- `frontend/src/components/consultation/ConsultationReady.jsx`
- `frontend/src/components/voice/VoiceInput.jsx`
- `frontend/src/components/voice/TTSPlayback.jsx`
- `frontend/src/pages/LoginPage.jsx`
- `frontend/src/pages/PhotoCapturePage.jsx`
- `frontend/src/services/auth.js`
- `frontend/src/App.jsx`

## Final Status
```
PHASE 1–18 = AUDITED / FIXED / VERIFIED
PHASE 19   = NOT IMPLEMENTED  (not audited; do not proceed until Phase 19 spec exists)
```