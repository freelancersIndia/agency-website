import hmac
import hashlib
from core.config.secrets import secrets_manager
from core.config.env_loader import get_settings
from shared.errors.exceptions import ValidationError

def validate_meta_signature(raw_payload: bytes, signature_header: str) -> None:
    """
    Validates that the incoming request payload matches the Meta X-Hub-Signature-256 header signature.
    """
    settings = get_settings()
    
    # Bypass signature check in local development if header is not present
    if settings.APP_ENV == "local" and not signature_header:
        return

    if not signature_header:
        raise ValidationError("Missing X-Hub-Signature-256 security header.")

    parts = signature_header.split("=")
    if len(parts) != 2 or parts[0] != "sha256":
        raise ValidationError("Invalid X-Hub-Signature-256 header format.")

    signature = parts[1]
    
    # Meta webhook payloads are signed using the App Secret or token
    meta_secret = secrets_manager.get_secret("META_TOKEN").encode("utf-8")
    
    computed = hmac.new(
        meta_secret,
        raw_payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed, signature):
        raise ValidationError("Meta webhook signature verification failed.")
