import uuid
from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    """
    Database model representing an ongoing chat session with a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=50, default="active")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "conversations"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Conversation {self.id} ({self.status})"

class Message(models.Model):
    """
    Database model representing an individual message exchange.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whatsapp_id = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True
    )
    sender_id = models.CharField(max_length=255)
    role = models.CharField(max_length=50)  # user, assistant, system, tool
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "messages"
        ordering = ["timestamp"]

    def __str__(self) -> str:
        return f"Message {self.id} - Role: {self.role}"

class Event(models.Model):
    """
    Database model tracking raw webhook event logs and status states.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=50, default="received", db_index=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "events"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Event {self.id} - Type: {self.event_type} ({self.status})"
