class MediKioskException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DatabaseConnectionError(MediKioskException):
    def __init__(self, message: str = "Could not connect to the database"):
        super().__init__(message, status_code=503)


class NotFoundError(MediKioskException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)
