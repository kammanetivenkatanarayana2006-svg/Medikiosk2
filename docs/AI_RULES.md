# MediKiosk - AI Safety Rules

## Core Principle
AI in MediKiosk is an **ASSISTIVE clinical documentation system** only.

## AI MUST NOT
- ❌ Autonomously diagnose medical conditions
- ❌ Confirm or rule out diseases
- ❌ Prescribe medications
- ❌ Change existing treatment plans
- ❌ Replace professional medical judgment
- ❌ Present unverified information as confirmed fact
- ❌ Finalize clinical reports without doctor verification
- ❌ Make clinical decisions independently
- ❌ Provide medical advice directly to patients
- ❌ Override doctor recommendations

## AI CAN (When Implemented)
- ✅ Assist in clinical documentation
- ✅ Transcribe patient responses
- ✅ Extract structured information from conversations
- ✅ Generate draft summaries for doctor review
- ✅ Suggest follow-up questions based on symptoms
- ✅ Flag potential urgent cases for priority review
- ✅ Organize and structure clinical information

## Mandatory Safeguards
1. All AI outputs must be clearly labeled as "Draft - Requires Doctor Verification"
2. Doctor review and approval is mandatory before finalization
3. AI confidence scores must be displayed when available
4. Source of information must be traceable
5. Patient consent is required for AI processing
6. Full audit trail of all AI interactions
# MediKiosk - AI Safety Rules

[Previous content preserved...]

## Local LLM (Phase 13)

### Model
- Qwen3 1.7B via Ollama
- Runs locally, no cloud LLM
- Patient data never leaves local environment

### AI May
- Ask follow-up questions
- Organize conversational context
- Identify missing information
- Assist interview flow
- Generate patient-friendly questions
- Respect selected language

### AI May NOT
- Diagnose
- Prescribe
- Recommend treatment
- Confirm diseases
- Replace doctor
- Finalize clinical history
- Make emergency decisions
- Access unrelated patient records
- Request authentication details
- Execute commands

### Prompt Injection Defense
- Patient responses treated as DATA only
- System rules immutable
- Output validated against schema
- Dangerous content rejected
- Deterministic fallback always available

### Statement
"MediKiosk uses local AI assistance for clinical information collection and documentation. AI-generated content is not a diagnosis or treatment recommendation and requires appropriate healthcare professional review."