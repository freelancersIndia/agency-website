from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from shared.types.dtos import MessageDTO
from shared.errors.exceptions import ValidationError

class WhatsAppPayloadParser:
    """
    Parses and normalizes raw Meta WhatsApp Webhook payloads into internal DTO representations.
    """
    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Tuple[str, Optional[MessageDTO], Optional[Dict[str, Any]]]:
        """
        Parses raw payload.
        Returns:
            Tuple[event_type, MessageDTO_if_message, status_update_dict_if_status]
            where event_type can be 'message', 'status', or 'unknown'.
        """
        # Top level validation
        if not payload or "entry" not in payload:
            return "unknown", None, None

        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Case 1: Status Updates (sent, delivered, read, failed)
                if "statuses" in value:
                    status_list = value.get("statuses", [])
                    if status_list:
                        status_data = status_list[0]
                        normalized_status = {
                            "message_id": status_data.get("id"),
                            "status": status_data.get("status"),
                            "timestamp": datetime.utcfromtimestamp(int(status_data.get("timestamp", 0))),
                            "recipient_id": status_data.get("recipient_id"),
                            "error": status_data.get("errors", [{}])[0].get("message") if "errors" in status_data else None
                        }
                        return "status", None, normalized_status

                # Case 2: Incoming Messages
                if "messages" in value:
                    message_list = value.get("messages", [])
                    if message_list:
                        msg_data = message_list[0]
                        sender_phone = msg_data.get("from")
                        msg_id = msg_data.get("id")
                        msg_type = msg_data.get("type", "text")
                        timestamp = datetime.utcfromtimestamp(int(msg_data.get("timestamp", datetime.now().timestamp())))
                        
                        profile_name = value.get("contacts", [{}])[0].get("profile", {}).get("name", "Unknown Contact")
                        
                        # Base metadata dictionary
                        meta = {
                            "profile_name": profile_name,
                            "type": msg_type
                        }
                        content = ""

                        # Parse based on message type
                        if msg_type == "text":
                            content = msg_data.get("text", {}).get("body", "")
                        elif msg_type == "reaction":
                            reaction = msg_data.get("reaction", {})
                            content = reaction.get("emoji", "")
                            meta["target_message_id"] = reaction.get("message_id")
                        elif msg_type in ["image", "video", "audio", "document"]:
                            media_data = msg_data.get(msg_type, {})
                            content = media_data.get("caption", f"Media attachment: {msg_type}")
                            meta["media_id"] = media_data.get("id")
                            meta["mime_type"] = media_data.get("mime_type")
                            if msg_type == "document":
                                meta["filename"] = media_data.get("filename", "document")
                        else:
                            content = f"Unsupported message type: {msg_type}"

                        # Map to MessageDTO
                        # Note: conversation_id is resolved as the sender's phone number
                        message_dto = MessageDTO(
                            id=msg_id,
                            conversation_id=sender_phone,
                            sender_id=sender_phone,
                            role="user",
                            content=content,
                            timestamp=timestamp,
                            metadata=meta
                        )
                        return "message", message_dto, None

        return "unknown", None, None
