import unittest
from datetime import datetime
from unittest.mock import MagicMock

from core.whatsapp.services.parser import WhatsAppPayloadParser
from core.whatsapp.validators import validate_meta_signature
from shared.utils.retry import execute_with_retry
from shared.errors.exceptions import ValidationError

class TestWhatsAppPayloadParser(unittest.TestCase):
    def test_parse_text_message(self) -> None:
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "contacts": [{"profile": {"name": "Test User"}, "wa_id": "12345"}],
                                "messages": [
                                    {
                                        "from": "12345",
                                        "id": "wamid.123",
                                        "timestamp": "1665396655",
                                        "type": "text",
                                        "text": {"body": "Hello World"}
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }
        event_type, msg_dto, status_dto = WhatsAppPayloadParser.parse_webhook_payload(payload)
        
        self.assertEqual(event_type, "message")
        self.assertIsNotNone(msg_dto)
        self.assertEqual(msg_dto.id, "wamid.123") # type: ignore
        self.assertEqual(msg_dto.sender_id, "12345") # type: ignore
        self.assertEqual(msg_dto.content, "Hello World") # type: ignore
        self.assertEqual(msg_dto.role, "user") # type: ignore

    def test_parse_status_update(self) -> None:
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "statuses": [
                                    {
                                        "id": "wamid.123",
                                        "status": "delivered",
                                        "timestamp": "1665396655",
                                        "recipient_id": "12345"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        event_type, msg_dto, status_dto = WhatsAppPayloadParser.parse_webhook_payload(payload)
        
        self.assertEqual(event_type, "status")
        self.assertIsNone(msg_dto)
        self.assertIsNotNone(status_dto)
        self.assertEqual(status_dto["message_id"], "wamid.123") # type: ignore
        self.assertEqual(status_dto["status"], "delivered") # type: ignore
        self.assertEqual(status_dto["recipient_id"], "12345") # type: ignore


class TestRetryHelper(unittest.TestCase):
    def test_retry_success(self) -> None:
        mock_func = MagicMock(return_value="success")
        res = execute_with_retry(mock_func, max_retries=2, initial_delay=0.01, backoff_factor=1)
        self.assertEqual(res, "success")
        self.assertEqual(mock_func.call_count, 1)

    def test_retry_failure_then_success(self) -> None:
        calls = []
        def mock_func():
            calls.append(1)
            if len(calls) < 2:
                raise ValueError("Temporary Error")
            return "recovered"

        res = execute_with_retry(mock_func, max_retries=2, initial_delay=0.01, backoff_factor=1)
        self.assertEqual(res, "recovered")
        self.assertEqual(len(calls), 2)

    def test_retry_permanent_failure(self) -> None:
        mock_func = MagicMock(side_effect=ValueError("Permanent Error"))
        with self.assertRaises(ValueError):
            execute_with_retry(mock_func, max_retries=2, initial_delay=0.01, backoff_factor=1)
        self.assertEqual(mock_func.call_count, 3) # initial attempt + 2 retries
