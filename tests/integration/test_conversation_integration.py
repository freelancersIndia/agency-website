from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from core.conversation.services.conversation_service import ConversationService
from core.conversation.models import Conversation, Message, Event

class TestConversationService(TestCase):
    def setUp(self) -> None:
        self.service = ConversationService()
        self.phone = "15555555555"
        self.customer_id = "test_customer"

    def test_conversation_lifecycle(self) -> None:
        # 1. Create conversation session
        conv = self.service.create_conversation(self.customer_id, self.phone)
        self.assertEqual(conv.customer_id, self.customer_id)
        self.assertEqual(conv.status, "active")

        # 2. Append incoming message
        msg = self.service.append_message(
            conversation_id=conv.id,
            sender_id=self.phone,
            role="user",
            content="Hello Platform!",
            whatsapp_id="wamid.test_lifecycle_id"
        )
        self.assertEqual(msg.content, "Hello Platform!")
        self.assertEqual(msg.conversation_id, conv.id)

        # 3. Assert database records count
        conv_db = Conversation.objects.get(id=conv.id)
        self.assertEqual(conv_db.messages.count(), 1)
        self.assertEqual(conv_db.messages.first().whatsapp_id, "wamid.test_lifecycle_id") # type: ignore

        # 4. Resolve conversation
        self.service.resolve_conversation(conv.id)
        conv_resolved = self.service.load_conversation(conv.id)
        self.assertIsNotNone(conv_resolved)
        self.assertEqual(conv_resolved.status, "resolved") # type: ignore


class TestWebhookAPI(APITestCase):
    def test_webhook_verification_handshake(self) -> None:
        url = reverse("whatsapp_webhook")
        
        # Meta verify token matches default test config value
        response = self.client.get(url, {
            "hub.mode": "subscribe",
            "hub.verify_token": "your-meta-whatsapp-cloud-api-token",
            "hub.challenge": "challenge_token_response"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "challenge_token_response")

    def test_webhook_post_ingest_message(self) -> None:
        url = reverse("whatsapp_webhook")
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "contacts": [{"profile": {"name": "E2E User"}, "wa_id": "19999999999"}],
                                "messages": [
                                    {
                                        "from": "19999999999",
                                        "id": "wamid.e2e_webhook_message_id",
                                        "timestamp": "1665396655",
                                        "type": "text",
                                        "text": {"body": "Automated End-to-End Test Payload"}
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }

        # Local mode bypasses signature headers
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Assert data was saved to database
        expected_uuid = ConversationService.get_conversation_uuid("19999999999")
        self.assertTrue(Conversation.objects.filter(id=expected_uuid).exists())
        self.assertTrue(Message.objects.filter(whatsapp_id="wamid.e2e_webhook_message_id").exists())
        self.assertTrue(Event.objects.filter(event_type="whatsapp").exists())
