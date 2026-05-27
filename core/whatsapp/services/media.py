import requests
from typing import Tuple
from core.config.secrets import secrets_manager
from core.config.env_loader import get_settings
from shared.errors.exceptions import ValidationError
from shared.logging.logger import logger

class WhatsAppMediaHandler:
    """
    Handles upload, download, and metadata queries for WhatsApp media objects.
    """
    def __init__(self) -> None:
        self.settings = get_settings()
        self.meta_token = secrets_manager.get_secret("META_TOKEN")
        self.phone_number_id = self.settings.META_PHONE_NUMBER_ID

    def get_media_metadata(self, media_id: str) -> Tuple[str, int, str]:
        """
        Fetches media download URL and details from Meta using the media ID.
        Returns: (url, file_size, mime_type)
        """
        url = f"https://graph.facebook.com/v18.0/{media_id}"
        headers = {
            "Authorization": f"Bearer {self.meta_token}"
        }

        # Mock result for offline local verification
        if self.settings.APP_ENV in ["local", "test"] and (
            self.meta_token.startswith("your-") or "mock" in self.meta_token or "default" in self.meta_token
        ):
            return "http://mock-server/download/file", 4096, "image/png"

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise ValidationError(f"Meta media query failed: {response.text}")

        res_data = response.json()
        return res_data["url"], res_data["file_size"], res_data["mime_type"]

    def download_media(self, media_id: str) -> Tuple[bytes, str]:
        """
        Downloads the media binary payload from Meta.
        Returns: (binary_content, mime_type)
        """
        url, _, mime_type = self.get_media_metadata(media_id)
        headers = {
            "Authorization": f"Bearer {self.meta_token}"
        }

        if url == "http://mock-server/download/file":
            return b"mock-media-binary-data", mime_type

        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise ValidationError(f"Failed to fetch media binary from Meta: {response.text}")

        return response.content, mime_type

    def upload_media(self, binary_content: bytes, filename: str, mime_type: str) -> str:
        """
        Uploads local binary data to Meta, acquiring a media ID for message attachments.
        """
        url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/media"
        headers = {
            "Authorization": f"Bearer {self.meta_token}"
        }

        if self.settings.APP_ENV in ["local", "test"] and (
            self.meta_token.startswith("your-") or "mock" in self.meta_token or "default" in self.meta_token
        ):
            logger.info(f"[MOCK MEDIA UPLOAD] Uploading file '{filename}' ({mime_type})")
            return "mock-uploaded-media-id"

        files = {
            "file": (filename, binary_content, mime_type)
        }
        data = {
            "messaging_product": "whatsapp",
            "type": mime_type
        }

        response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        if response.status_code != 200:
            raise ValidationError(f"Failed to upload media file to Meta: {response.text}")

        return response.json().get("id")
