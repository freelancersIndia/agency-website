import os
from typing import Dict
from core.config.env_loader import get_settings
from shared.logging.logger import logger
from shared.errors.exceptions import ValidationError

class SecretsManager:
    """
    Manages loading, validating, and dynamic rotation overrides for sensitive system keys.
    """
    def __init__(self) -> None:
        self._settings = get_settings()
        self._cache: Dict[str, str] = {}

    def get_secret(self, name: str) -> str:
        """
        Retrieves a secret dynamically, prioritizing memory cache overrides then env parameters.
        """
        # Dynamic cache lookup
        if name in self._cache:
            return self._cache[name]

        # Fetch from standard settings schema
        val = getattr(self._settings, name, None)
        if not val:
            # Fallback to direct environment query
            val = os.getenv(name)

        if not val:
            raise ValidationError(f"Secret parameter '{name}' is missing or not configured.")

        return val

    def rotate_secret(self, name: str, new_value: str) -> None:
        """
        Updates a secret parameter in-memory to support dynamic key rotation without restart.
        """
        cleaned_val = new_value.strip()
        if not cleaned_val or len(cleaned_val) < 16:
            raise ValidationError(f"Dynamic override for '{name}' fails basic security strength requirements.")

        logger.info(f"Secret parameter '{name}' rotated successfully in memory.")
        self._cache[name] = cleaned_val

    def verify_security_postures(self) -> None:
        """
        Asserts that environment secrets do not use placeholders or insecure defaults in non-local scopes.
        """
        env = self._settings.APP_ENV
        keys_to_verify = ["DJANGO_SECRET", "FASTAPI_SECRET", "OPENAI_KEY", "META_TOKEN", "EMAIL_KEY"]

        for key in keys_to_verify:
            val = self.get_secret(key)
            if env != "local":
                if len(val) < 16:
                    raise ValidationError(f"Security Warning: Secret '{key}' is too short for non-local environment '{env}' usage.")
                
                lowered_val = val.lower()
                placeholders = ["default", "change-me", "insecure", "mock", "your-openai", "your-meta", "your-email"]
                if any(p in lowered_val for p in placeholders):
                    raise ValidationError(f"Security Alert: Secret '{key}' contains insecure placeholders in non-local scope.")

# Shared Singleton Instance
secrets_manager = SecretsManager()
