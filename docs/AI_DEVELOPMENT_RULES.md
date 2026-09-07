# MediKiosk - AI Development Rules

## Purpose
This document provides mandatory rules for AI coding assistants working on the MediKiosk project. These rules ensure consistency, safety, and quality across all development phases.

## Critical Rules

### 1. Project Inspection
- ✅ ALWAYS inspect the existing project structure first
- ✅ Read all documentation in `docs/` before making changes
- ✅ Check `docs/PHASE_STATUS.md` to understand current progress
- ✅ Verify existing functionality before modifications
- ❌ NEVER assume previous code is missing or broken without verification

### 2. Documentation First
- Read these files in order:
  1. `docs/PROJECT_CONTEXT.md`
  2. `docs/ARCHITECTURE.md`
  3. `docs/PHASE_STATUS.md`
  4. `docs/API_CONTRACT.md`
  5. `docs/AI_RULES.md`
  6. `docs/SECURITY_RULES.md`

### 3. Phase Discipline
- ✅ Implement ONLY the requested phase
- ❌ NEVER implement future phases
- ❌ NEVER add "helpful" features from later phases
- ✅ If unsure about scope, ask for clarification

### 4. Code Preservation
- ✅ Preserve working functionality
- ❌ NEVER rewrite working code unnecessarily
- ✅ Make minimal, targeted changes
- ✅ Maintain backward compatibility when practical

### 5. API Stability
- ✅ Preserve existing API endpoints
- ✅ Document all API changes
- ✅ Use version prefixes for new APIs
- ❌ NEVER break existing API contracts

### 6. Dependency Management
- ✅ Check existing dependencies first
- ✅ Install only what's needed for current phase
- ❌ NEVER add unnecessary dependencies
- ❌ NEVER upgrade all packages blindly
- ✅ Document new dependencies and their purpose

### 7. Security
- ❌ NEVER hardcode secrets
- ❌ NEVER commit API keys or passwords
- ✅ Use environment variables for configuration
- ✅ Follow `SECURITY_RULES.md` guidelines
- ✅ Consider security implications of all changes

### 8. Testing
- ✅ Run tests after every change
- ✅ Test both frontend and backend
- ✅ Verify API endpoints work
- ✅ Check for syntax and import errors
- ❌ NEVER claim success without testing
- ❌ NEVER leave known errors unresolved

### 9. Documentation Updates
- ✅ Update `PHASE_STATUS.md` after completion
- ✅ Update relevant documentation when architecture changes
- ✅ Document new endpoints and features
- ✅ Keep documentation consistent with code

### 10. Code Quality
- ✅ Write clean, readable code
- ✅ Use meaningful variable and function names
- ✅ Add comments only where useful
- ❌ NO dead code
- ❌ NO fake implementations
- ❌ NO placeholder logic pretending to be functional

### 11. Medical AI Safety
- ✅ AI is ASSISTIVE only
- ✅ Doctor verification is mandatory
- ❌ AI never makes autonomous decisions
- ❌ AI never provides final diagnosis
- ✅ Follow `AI_RULES.md` strictly

### 12. Change Management
Follow this workflow:
1. **Inspect** - Understand current state
2. **Plan** - Define changes needed
3. **Implement** - Make changes
4. **Test** - Verify changes work
5. **Review** - Check for issues
6. **Document** - Update docs
7. **Report** - Summarize changes

### 13. Error Handling
- ✅ Diagnose errors thoroughly
- ✅ Fix root causes, not symptoms
- ✅ Test fixes before moving on
- ❌ NEVER skip error resolution
- ❌ NEVER report errors without fixing them

### 14. Data Privacy
- ❌ NEVER expose patient data unnecessarily
- ❌ NEVER log sensitive information
- ✅ Minimize data collection
- ✅ Implement proper access controls

### 15. Reporting
- ✅ Provide accurate status reports
- ✅ List all files changed
- ✅ Document all errors found and fixed
- ❌ NEVER claim success without verification