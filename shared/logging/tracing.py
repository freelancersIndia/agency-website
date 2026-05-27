import threading
import uuid
from typing import Optional

_thread_local = threading.local()

def set_request_id(request_id: str) -> None:
    """
    Saves a request ID to the current thread-local context.
    """
    _thread_local.request_id = request_id

def get_request_id() -> Optional[str]:
    """
    Retrieves the request ID from the current thread-local context.
    """
    return getattr(_thread_local, "request_id", None)

def clear_request_id() -> None:
    """
    Clears the request ID from the current thread-local context.
    """
    if hasattr(_thread_local, "request_id"):
        del _thread_local.request_id

def generate_request_id() -> str:
    """
    Generates a new unique request ID.
    """
    return str(uuid.uuid4())
