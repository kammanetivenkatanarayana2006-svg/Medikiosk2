# MediKiosk - Database Schema & Architecture

## Database Foundation (Phase 3)

### Connection Management
- **Driver:** Motor (async MongoDB driver)
- **Connection:** Singleton pattern with lifecycle management
- **Pooling:** Connection pool with configurable size (default: 10)
- **Timeout:** 5-second connection timeout
- **Graceful Degradation:** Application runs without database if unavailable

### ObjectId Strategy
- **MongoDB `_id`:** Internal database identifier (ObjectId)
- **Human-readable IDs:** Separate fields (future: `op_number`, `patient_id`, etc.)
- **Never use:** ObjectId as external identifier
- **Always store:** Human-readable IDs as separate indexed fields

## Planned Collections (Future Phases)

### 1. users
**Purpose:** Store user accounts and authentication data
**Important Fields:**
- `_id`: ObjectId (internal)
- `email`: String (normalized, unique)
- `phone`: String (normalized, unique)
- `password_hash`: String
- `role`: Enum ["admin", "doctor", "patient", "staff"]
- `is_active`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

**Relationships:** None (base entity)
**Indexes:** 
- `email` (unique)
- `phone` (unique)
- `role` (non-unique)

### 2. patients
**Purpose:** Store patient profile and demographic information
**Important Fields:**
- `_id`: ObjectId (internal)
- `user_id`: ObjectId (references users)
- `patient_identifier`: String (human-readable, unique)
- `full_name`: String
- `date_of_birth`: Date
- `gender`: Enum
- `blood_group`: String
- `allergies`: Array
- `emergency_contact`: Object

**Relationships:**
- Belongs to: User (1:1)
- Has many: Consultations, Medical Reports

**Indexes:**
- `patient_identifier` (unique)
- `user_id` (unique)
- `full_name` (text index)

### 3. doctors
**Purpose:** Store doctor profile and specialization
**Important Fields:**
- `_id`: ObjectId (internal)
- `user_id`: ObjectId (references users)
- `doctor_identifier`: String (human-readable, unique)
- `full_name`: String
- `specialization`: String
- `registration_number`: String
- `years_of_experience`: Number
- `availability`: Object

**Relationships:**
- Belongs to: User (1:1)
- Has many: Consultations

**Indexes:**
- `doctor_identifier` (unique)
- `user_id` (unique)
- `specialization` (non-unique)

### 4. consultations
**Purpose:** Store consultation records and workflow state
**Important Fields:**
- `_id`: ObjectId (internal)
- `op_number`: String (human-readable, unique)
- `patient_id`: ObjectId (references patients)
- `doctor_id`: ObjectId (references doctors, optional)
- `status`: Enum ["pending", "in_progress", "completed", "cancelled"]
- `priority`: Enum ["low", "medium", "high", "emergency"]
- `symptoms`: Array
- `started_at`: DateTime
- `completed_at`: DateTime

**Relationships:**
- Belongs to: Patient (N:1)
- Assigned to: Doctor (N:1, optional)
- Has one: Clinical History
- Has many: Medical Reports, AI Summaries

**Indexes:**
- `op_number` (unique)
- `patient_id` (non-unique)
- `doctor_id` (non-unique)
- `status` (non-unique)
- `created_at` (non-unique, descending)

### 5. medical_reports
**Purpose:** Store uploaded medical reports and OCR results
**Important Fields:**
- `_id`: ObjectId (internal)
- `patient_id`: ObjectId (references patients)
- `consultation_id`: ObjectId (references consultations, optional)
- `file_path`: String
- `file_type`: String
- `ocr_text`: String
- `report_date`: Date
- `uploaded_at`: DateTime

**Relationships:**
- Belongs to: Patient (N:1)
- Related to: Consultation (N:1, optional)

**Indexes:**
- `patient_id` (non-unique)
- `consultation_id` (non-unique)
- `uploaded_at` (non-unique, descending)

### 6. clinical_histories
**Purpose:** Store extracted clinical information from AI interviews
**Important Fields:**
- `_id`: ObjectId (internal)
- `consultation_id`: ObjectId (references consultations)
- `patient_id`: ObjectId (references patients)
- `chief_complaint`: String
- `symptoms`: Array
- `medical_history`: Object
- `medications`: Array
- `allergies`: Array
- `extracted_at`: DateTime

**Relationships:**
- Belongs to: Consultation (1:1)
- Related to: Patient (N:1)

**Indexes:**
- `consultation_id` (unique)
- `patient_id` (non-unique)

### 7. ai_summaries
**Purpose:** Store AI-generated clinical summaries
**Important Fields:**
- `_id`: ObjectId (internal)
- `consultation_id`: ObjectId (references consultations)
- `summary_text`: String
- `confidence_score`: Number
- `is_verified`: Boolean
- `verified_by`: ObjectId (references doctors)
- `verified_at`: DateTime
- `created_at`: DateTime

**Relationships:**
- Belongs to: Consultation (N:1)
- Verified by: Doctor (N:1)

**Indexes:**
- `consultation_id` (non-unique)
- `is_verified` (non-unique)

### 8. audit_logs
**Purpose:** Store system audit trail
**Important Fields:**
- `_id`: ObjectId (internal)
- `user_id`: ObjectId (references users)
- `action`: String
- `entity_type`: String
- `entity_id`: ObjectId
- `timestamp`: DateTime
- `ip_address`: String
- `metadata`: Object

**Relationships:** None (append-only log)

**Indexes:**
- `user_id` (non-unique)
- `timestamp` (non-unique, descending)
- `action` (non-unique)

### 9. follow_ups
**Purpose:** Store follow-up appointments and reminders
**Important Fields:**
- `_id`: ObjectId (internal)
- `consultation_id`: ObjectId (references consultations)
- `patient_id`: ObjectId (references patients)
- `scheduled_at`: DateTime
- `status`: Enum ["scheduled", "completed", "cancelled"]
- `notes`: String
- `reminder_sent`: Boolean

**Relationships:**
- Belongs to: Consultation (N:1)
- Related to: Patient (N:1)

**Indexes:**
- `scheduled_at` (non-unique)
- `status` (non-unique)
- `patient_id` (non-unique)

## Conceptual Relationships
## patients Collection (Phase 9)

### Purpose
Store patient profile information separate from authentication data.

### Fields
- `_id`: ObjectId (internal)
- `user_id`: String (references users collection)
- `full_name`: String
- `email`: String (normalized)
- `phone`: String (10 digits)
- `gender`: String (Male/Female/Other/Prefer not to say)
- `age`: Number (optional)
- `date_of_birth`: String (optional)
- `photo_reference`: String (generated ID, not user filename)
- `photo_consent`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

### Indexes
- `user_id` (unique)
- `email` (unique)
- `phone` (unique)

### Photo Storage
- Photos stored separately from database
- Database stores reference ID only
- Generated random identifiers (no PII in filenames)
## clinical_extractions Collection (Phase 14)

### Purpose
Store AI-extracted structured clinical information from patient responses.

### Fields
- `_id`: ObjectId
- `interview_id`: String
- `consultation_id`: String
- `patient_id`: String
- `response_id`: String (unique)
- `question_id`: String
- `section`: String
- `extracted_fields`: Object (structured clinical data)
- `source`: String ("ai_extracted")
- `extraction_version`: Number
- `status`: String (pending/processing/completed/failed/needs_review)
- `created_at`: DateTime
- `updated_at`: DateTime

### Indexes
- `response_id` (unique)
- `interview_id`
- `consultation_id`
- `patient_id`
- `status`

## medical_documents Collection (Phase 15)

### Fields
- `_id`: ObjectId
- `patient_id`: String
- `user_id`: String
- `consultation_id`: String (optional)
- `original_filename`: String
- `document_type`: String (pdf/image)
- `mime_type`: String
- `file_size`: Number
- `storage_key`: String (generated)
- `ocr_status`: String (pending/processing/completed/failed)
- `processing_status`: String
- `uploaded_at`: DateTime
- `updated_at`: DateTime

## ocr_results Collection (Phase 15)

### Fields
- `_id`: ObjectId
- `medical_document_id`: String
- `patient_id`: String
- `consultation_id`: String (optional)
- `text`: String (extracted)
- `page_count`: Number
- `language`: String (nullable)
- `ocr_provider`: String
- `status`: String
- `created_at`: DateTime
- `updated_at`: DateTime