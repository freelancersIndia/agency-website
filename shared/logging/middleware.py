import time
from typing import Callable
from django.http import HttpRequest, HttpResponse
from shared.logging.logger import logger

class DjangoRequestLoggingMiddleware:
    """
    Django middleware to log route request details, duration, and status codes.
    """
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        
        path = request.path
        method = request.method
        
        # Process the request
        response = self.get_response(request)
        
        duration = time.time() - start_time
        status_code = response.status_code
        
        # Compile structure data for logging
        log_context = {
            "extra": {
                "http_method": method,
                "http_path": path,
                "status_code": status_code,
                "duration_ms": int(duration * 1000)
            }
        }
        
        log_message = f"HTTP {method} {path} - Status: {status_code} in {duration * 1000:.2f}ms"
        
        if status_code >= 500:
            logger.error(log_message, exc_info=True, extra=log_context)
        elif status_code >= 400:
            logger.warning(log_message, extra=log_context)
        else:
            logger.info(log_message, extra=log_context)
            
        return response

