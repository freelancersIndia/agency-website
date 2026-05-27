from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from shared.types.dtos import MessageDTO, ConversationDTO, ToolExecutionDTO

class BaseAgentExecutor(ABC):
    """
    Abstract Interface defining operations for AI Agent planning and execution.
    """
    @abstractmethod
    def execute(self, conversation_id: str, message: MessageDTO) -> MessageDTO:
        """
        Executes an agent reasoning loop and returns the assistant message DTO outcome.
        """
        pass

class BaseKnowledgeRetriever(ABC):
    """
    Abstract Interface defining retrieval strategies inside RAG modules.
    """
    @abstractmethod
    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Queries underlying pgvector stores and returns matching documents chunks.
        """
        pass

class BaseConversationRepository(ABC):
    """
    Abstract Interface defining persistence transactions for session events.
    """
    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Optional[ConversationDTO]:
        """
        Fetches metadata attributes of a conversation.
        """
        pass

    @abstractmethod
    def save_message(self, message: MessageDTO) -> None:
        """
        Persists a newly exchanged message event to storage.
        """
        pass

class BaseTool(ABC):
    """
    Abstract Interface representing an executable action tool exposed to agents.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the unique identifier of the tool.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Returns helper description details for system prompts.
        """
        pass

    @abstractmethod
    def execute(self, payload: ToolExecutionDTO) -> ToolExecutionDTO:
        """
        Executes action logic and updates payload parameters with results.
        """
        pass
