from typing import Callable
from django.http import HttpRequest, HttpResponse, JsonResponse
from shared.errors.exceptions import AppError
from shared.logging.logger import logger

class DjangoGlobalExceptionMiddleware:
    """
    Middleware to capture application exceptions and return formatted JSON error messages.
    """
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> JsonResponse:
        """
        Intercepts raised exceptions and maps them to custom status payloads.
        """
        if isinstance(exception, AppError):
            status_code = exception.status_code
            error_code = exception.error_code
            message = exception.message
            logger.warning(f"Domain Exception: {message} ({error_code})")
        else:
            status_code = 500
            error_code = "UNEXPECTED_ERROR"
            message = "An unexpected server error occurred."
            logger.error(f"Unhandled Exception: {str(exception)}", exc_info=exception)

        payload = {
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
            }
        }
        return JsonResponse(payload, status=status_code)
