import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """
    Custom formatter that transforms Python log records into structured JSON payloads.
    """
    def format(self, record: logging.LogRecord) -> str:
        from shared.logging.tracing import get_request_id
        
        log_payload: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "file": f"{record.pathname}:{record.lineno}"
        }
        
        req_id = get_request_id()
        if req_id:
            log_payload["request_id"] = req_id

        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        # Ingest extra context if attached to the record
        if hasattr(record, "extra") and isinstance(record.extra, dict): # type: ignore
            log_payload.update(record.extra) # type: ignore

        return json.dumps(log_payload)

def get_platform_logger(name: str = "whatsapp_platform") -> logging.Logger:
    """
    Fetches or creates a structured console logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Enforce capture of debug, info, warn, error
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger

# Shared default logger instance
logger = get_platform_logger()
