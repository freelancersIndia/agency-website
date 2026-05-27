from django.urls import path
from apps.webhook.views import WhatsAppWebhookView, OutgoingMessageView, ConversationDetailView

urlpatterns = [
    path("webhook", WhatsAppWebhookView.as_view(), name="whatsapp_webhook"),
    path("messages/send", OutgoingMessageView.as_view(), name="outgoing_messages"),
    path("conversations/<str:conversation_id>", ConversationDetailView.as_view(), name="conversation_detail"),
]
