# MediKiosk - Security Rules

## Security Principles

### Data Protection
- All patient data is sensitive and must be protected
- Encryption at rest for all stored data
- Encryption in transit (HTTPS) mandatory
- Data minimization - collect only what's needed

### Authentication & Authorization
- JWT-based authentication (future phase)
- Role-based access control (RBAC)
- Session management with expiry
- Password hashing with bcrypt/argon2
- Rate limiting on authentication endpoints

### API Security
- Input validation on all endpoints
- SQL/NoSQL injection prevention
- XSS protection
- CSRF protection
- API key rotation for external services

### Audit & Compliance
- Comprehensive audit logging
- All data access must be logged
- HIPAA-inspired data handling practices
- Data retention policies
- Right to erasure support

### Infrastructure Security
- Secrets management via environment variables
- No hardcoded credentials
- Regular security updates
- Dependency vulnerability scanning
- Secure configuration defaults

### Privacy by Design
- Consent management
- Data anonymization where possible
- Transparent data usage policies
- User data export capability
- Deletion on request
# MediKiosk - Security Rules

[Previous content preserved...]

## OTP Security (Phase 8)

### OTP Storage
- Never store plaintext OTP
- Always store SHA-256 hash
- Never log OTP values
- Never return OTP in API response

### OTP Expiry
- OTP expires after configurable period (default: 10 minutes)
- Expired OTP cannot be used
- Expired OTP records cleaned via TTL index

### OTP Attempts
- Maximum 5 verification attempts
- After max attempts, OTP invalidated
- New OTP required after invalidation

### OTP Resend
- 30-second cooldown between resends
- Previous OTP invalidated on resend
- Rate limiting recommended for production

## Email Verification Security
- Secure random token (URL-safe, 32 bytes)
- Token stored as SHA-256 hash
- Token expires after 24 hours
- Token is single-use
- Token invalidated after successful verification

## Notification Privacy
- No passwords in emails/WhatsApp
- No OTP in login notifications
- No medical data in notifications
- Minimal information in messages
- Provider failures logged without sensitive data