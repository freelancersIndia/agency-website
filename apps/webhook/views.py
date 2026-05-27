import json
import uuid
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.whatsapp.validators import validate_meta_signature
from core.whatsapp.services.parser import WhatsAppPayloadParser
from core.whatsapp.services.sender import WhatsAppMessageSender
from core.conversation.services.conversation_service import ConversationService
from core.conversation.repositories import MessageRepository
from core.conversation.models import Event
from shared.logging.logger import logger

class WhatsAppWebhookView(APIView):
    """
    Ingests WhatsApp incoming message webhook requests from Meta.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_service = ConversationService()
        self.message_repo = MessageRepository()

    def get(self, request, *args, **kwargs):
        """
        Verification verification handshake from Meta Cloud API settings.
        """
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        from core.config.secrets import secrets_manager
        verify_token = secrets_manager.get_secret("META_TOKEN")

        if mode == "subscribe" and token == verify_token:
            logger.info("Webhook endpoint successfully verified by Meta API.")
            return HttpResponse(challenge, content_type="text/plain")

        logger.warning("Verification handshake failed: token mismatch.")
        return Response({"error": "Forbidden Verification"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        """
        Meta Webhook POST event listener.
        """
        raw_body = request.body
        signature = request.headers.get("X-Hub-Signature-256", "")

        try:
            validate_meta_signature(raw_body, signature)
        except Exception as e:
            logger.warning(f"Rejecting payload. Webhook signature error: {str(e)}")
            return Response({"error": "Forbidden Verification"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            return Response({"error": "Invalid payload JSON"}, status=status.HTTP_400_BAD_REQUEST)

        # Log raw event payload
        event_obj = Event.objects.create(
            event_type="whatsapp",
            status="received",
            payload=payload
        )

        event_type, msg_dto, status_dto = WhatsAppPayloadParser.parse_webhook_payload(payload)

        try:
            if event_type == "message" and msg_dto:
                # 1. Create or reopen conversation
                conv = self.conversation_service.create_conversation(
                    customer_id="default_customer",
                    phone=msg_dto.sender_id,
                    metadata=msg_dto.metadata
                )
                # 2. Append message event to conversation
                self.conversation_service.append_message(
                    conversation_id=conv.id,
                    sender_id=msg_dto.sender_id,
                    role=msg_dto.role,
                    content=msg_dto.content,
                    whatsapp_id=msg_dto.id,
                    metadata=msg_dto.metadata
                )
                event_obj.status = "processed"
                event_obj.save()
            elif event_type == "status" and status_dto:
                whatsapp_id = status_dto.get("message_id")
                msg = self.message_repo.find_by_whatsapp_id(whatsapp_id)
                if msg:
                    msg.metadata["delivery_status"] = status_dto.get("status")
                    self.message_repo.save(msg)
                event_obj.status = "processed"
                event_obj.save()
        except Exception as e:
            logger.error(f"Error processing webhook payload: {str(e)}", exc_info=True)
            event_obj.status = "failed"
            event_obj.save()

        # Meta expects HTTP 200 response <500ms
        return Response({"success": True}, status=status.HTTP_200_OK)

class OutgoingMessageView(APIView):
    """
    Exposes POST /api/v1/messages/send to send messages outbound.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = WhatsAppMessageSender()

    def post(self, request, *args, **kwargs):
        recipient = request.data.get("to")
        message_body = request.data.get("message")
        template_name = request.data.get("template")
        reply_to = request.data.get("reply_to")

        if not recipient:
            return Response({"error": "Recipient parameter 'to' is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if template_name:
                res = self.sender.send_template(recipient, template_name)
            elif message_body:
                res = self.sender.send_text(recipient, message_body, reply_to_message_id=reply_to)
            else:
                return Response({"error": "Either 'message' or 'template' parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": True, "result": res}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to submit message: {str(e)}")
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationDetailView(APIView):
    """
    Exposes GET /api/v1/conversations/{id} to retrieve session data.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_service = ConversationService()

    def get(self, request, conversation_id, *args, **kwargs):
        conv = self.conversation_service.load_conversation(conversation_id)
        if not conv:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": conv.id,
            "customer_id": conv.customer_id,
            "status": conv.status,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "metadata": conv.metadata
        })
