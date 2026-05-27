class AppError(Exception):
    """
    Base application exception from which all domain-specific errors inherit.
    """
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_SERVER_ERROR"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class ValidationError(AppError):
    """
    Exception raised when request payloads fail input or schema validation checks.
    """
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, status_code=400, error_code=error_code)

class InfrastructureError(AppError):
    """
    Exception raised when databases, caches, or external third-party APIs fail.
    """
    def __init__(self, message: str, error_code: str = "INFRASTRUCTURE_ERROR"):
        super().__init__(message, status_code=502, error_code=error_code)
