from src.schemas.chat import UserMessage, AssistantMessage, Chat, ChatRequest, ChatResponse
from src.llm.llm_registry import LLMRegistry
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChatService:
    def __init__(self):
        self.llm_registry = LLMRegistry()

    def generate_chat_completion(self, chat_request: ChatRequest) -> ChatResponse:
        """Generate a chat completion from a user message."""

        user_message = chat_request.message
        
        llm_model = self.llm_registry.get_model(chat_request.model_id)
        llm_response = llm_model.get_completion(
            message=user_message.content
        )

        assistant_message = AssistantMessage(
            role=AssistantMessage.role,
            content=llm_response
        )

        # Create a new chat object
        chat = Chat(
            id=1,  # This would typically be auto-incremented in a database
            conversation_id=chat_request.conversation_id,
            message=user_message,
            created_at=datetime.now().isoformat()
        )


        chat_response = ChatResponse(
            conversation_id=chat_request.conversation_id,
            message=assistant_message,
            model_id=chat_request.model_id
        )
        return chat_response