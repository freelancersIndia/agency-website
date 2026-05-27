import requests
from typing import Any, Dict, Optional
from core.config.secrets import secrets_manager
from core.config.env_loader import get_settings
from shared.logging.logger import logger
from shared.utils.retry import execute_with_retry
from shared.errors.exceptions import ValidationError

class WhatsAppMessageSender:
    """
    Outbound message gateway sending JSON payloads to Meta Cloud API endpoints.
    """
    def __init__(self) -> None:
        self.settings = get_settings()
        self.meta_token = secrets_manager.get_secret("META_TOKEN")
        self.phone_number_id = self.settings.META_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"

    def send_raw_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits HTTP POST requests to Meta with validation and retry wrappers.
        """
        headers = {
            "Authorization": f"Bearer {self.meta_token}",
            "Content-Type": "application/json"
        }

        def _call_api() -> Dict[str, Any]:
            # Bypass external calls during offline local verification or if mock tokens are loaded
            if self.settings.APP_ENV in ["local", "test"] and (
                self.meta_token.startswith("your-") or "mock" in self.meta_token or "default" in self.meta_token
            ):
                logger.info(f"[MOCK METADATA SEND] Intercepted payload: {payload}")
                return {"messaging_product": "whatsapp", "contacts": [{"input": payload.get("to"), "wa_id": payload.get("to")}], "messages": [{"id": "wamid.HBgM..."}]}

            response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code >= 400:
                logger.error(f"WhatsApp Meta API request failed with code {response.status_code}: {response.text}")
                raise ValidationError(f"Meta API endpoint error ({response.status_code}): {response.text}")

            return response.json()

        return execute_with_retry(_call_api)

    def send_text(self, recipient_phone: str, text: str, reply_to_message_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Constructs and sends a standard text payload, supporting contextual reply mapping.
        """
        payload: Dict[str, Any] = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "body": text
            }
        }
        if reply_to_message_id:
            payload["context"] = {
                "message_id": reply_to_message_id
            }

        return self.send_raw_payload(payload)

    def send_template(self, recipient_phone: str, template_name: str, language_code: str = "en_US") -> Dict[str, Any]:
        """
        Constructs and sends standard Meta template-based messages.
        """
        payload: Dict[str, Any] = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        return self.send_raw_payload(payload)
