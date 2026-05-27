import uuid
from typing import Optional
from core.conversation.models import Conversation, Message, Event

class ConversationRepository:
    """
    Data access repository for conversation entities.
    """
    def find_by_id(self, conv_id: uuid.UUID) -> Optional[Conversation]:
        try:
            return Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            return None

    def save(self, conversation: Conversation) -> None:
        conversation.save()

class MessageRepository:
    """
    Data access repository for message entities.
    """
    def find_by_whatsapp_id(self, whatsapp_id: str) -> Optional[Message]:
        try:
            return Message.objects.get(whatsapp_id=whatsapp_id)
        except Message.DoesNotExist:
            return None

    def save(self, message: Message) -> None:
        message.save()

class EventRepository:
    """
    Data access repository for audit and webhook events log records.
    """
    def save(self, event: Event) -> None:
        event.save()
