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
        from shared.logging.tracing import set_request_id, clear_request_id, generate_request_id
        
        # Read from header or generate a new one
        request_id = request.headers.get("X-Request-ID") or generate_request_id()
        set_request_id(request_id)
        
        start_time = time.time()
        
        path = request.path
        method = request.method
        
        try:
            # Process the request
            response = self.get_response(request)
        finally:
            duration = time.time() - start_time
            status_code = getattr(response, "status_code", 500) if 'response' in locals() else 500
            
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
                
            clear_request_id()
            
        if 'response' in locals():
            response["X-Request-ID"] = request_id
            return response
        else:
            from django.http import JsonResponse
            return JsonResponse({"error": "Server error"}, status=500)

