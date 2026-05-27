import uuid
from typing import Optional
from django.db import transaction
from core.conversation.models import Conversation, Message
from core.conversation.repositories import ConversationRepository, MessageRepository
from shared.types.dtos import MessageDTO, ConversationDTO
from shared.errors.exceptions import ValidationError

class ConversationService:
    """
    Handles business workflows and state transitions of the Conversation lifecycle.
    """
    def __init__(
        self,
        conversation_repo: Optional[ConversationRepository] = None,
        message_repo: Optional[MessageRepository] = None
    ) -> None:
        self.conversation_repo = conversation_repo or ConversationRepository()
        self.message_repo = message_repo or MessageRepository()

    @staticmethod
    def get_conversation_uuid(phone: str) -> uuid.UUID:
        """
        Derives a unique, deterministic UUID for a contact phone number namespace.
        """
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"whatsapp.phone.{phone}")

    def create_conversation(self, customer_id: str, phone: str, metadata: Optional[dict] = None) -> ConversationDTO:
        """
        Initializes a conversation session if it doesn't exist, resetting resolved state if needed.
        """
        conv_id = self.get_conversation_uuid(phone)
        with transaction.atomic():
            conv = self.conversation_repo.find_by_id(conv_id)
            if not conv:
                conv = Conversation(
                    id=conv_id,
                    customer_id=customer_id,
                    status="active",
                    metadata=metadata or {}
                )
                self.conversation_repo.save(conv)
            elif conv.status == "resolved":
                conv.status = "active"
                self.conversation_repo.save(conv)

            return ConversationDTO(
                id=str(conv.id),
                customer_id=conv.customer_id,
                status=conv.status,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                metadata=conv.metadata
            )

    def load_conversation(self, conversation_id: str) -> Optional[ConversationDTO]:
        """
        Loads the current conversation details by its unique identifier.
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            conv = self.conversation_repo.find_by_id(conv_uuid)
            if not conv:
                return None
            return ConversationDTO(
                id=str(conv.id),
                customer_id=conv.customer_id,
                status=conv.status,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                metadata=conv.metadata
            )
        except (ValueError, Conversation.DoesNotExist):
            return None

    def append_message(
        self,
        conversation_id: str,
        sender_id: str,
        role: str,
        content: str,
        whatsapp_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> MessageDTO:
        """
        Appends a message log to an active conversation, updating its timestamp context.
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            conv = self.conversation_repo.find_by_id(conv_uuid)
        except ValueError:
            raise ValidationError(f"Invalid UUID format: '{conversation_id}'")

        if not conv:
            raise ValidationError(f"Conversation with id '{conversation_id}' does not exist.")

        with transaction.atomic():
            msg = None
            if whatsapp_id:
                msg = self.message_repo.find_by_whatsapp_id(whatsapp_id)

            if not msg:
                msg = Message(
                    whatsapp_id=whatsapp_id,
                    conversation=conv,
                    sender_id=sender_id,
                    role=role,
                    content=content,
                    metadata=metadata or {}
                )
                self.message_repo.save(msg)
                
            # Touch parent conversation to update timestamps
            self.conversation_repo.save(conv)

            return MessageDTO(
                id=whatsapp_id or str(msg.id),
                conversation_id=str(conv.id),
                sender_id=sender_id,
                role=role,
                content=content,
                timestamp=msg.timestamp,
                metadata=msg.metadata
            )

    def resolve_conversation(self, conversation_id: str) -> None:
        """
        Resolves a conversation session, moving it to historical archives.
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            conv = self.conversation_repo.find_by_id(conv_uuid)
        except ValueError:
            raise ValidationError(f"Invalid UUID format: '{conversation_id}'")

        if not conv:
            raise ValidationError(f"Conversation with id '{conversation_id}' does not exist.")

        conv.status = "resolved"
        self.conversation_repo.save(conv)
