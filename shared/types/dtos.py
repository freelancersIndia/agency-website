from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class MessageDTO(BaseModel):
    """
    Data Transfer Object representing a text or media message exchange event.
    """
    id: str
    conversation_id: str
    sender_id: str
    role: str = Field(description="Role of the message author (user, assistant, system, tool)")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ConversationDTO(BaseModel):
    """
    Data Transfer Object holding conversation session attributes.
    """
    id: str
    customer_id: str
    status: str = Field(default="active")
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentRequestDTO(BaseModel):
    """
    Payload model sent to invoke the FastAPI AI reasoning runtime.
    """
    conversation_id: str
    user_message_id: str
    content: str
    customer_id: str
    context_overrides: Dict[str, Any] = Field(default_factory=dict)

class ToolExecutionDTO(BaseModel):
    """
    Standard interface payload detailing tool requests and outcomes.
    """
    tool_name: str
    arguments: Dict[str, Any]
    execution_id: str
    status: str = Field(default="pending")
    result: Optional[str] = None
    error: Optional[str] = None
