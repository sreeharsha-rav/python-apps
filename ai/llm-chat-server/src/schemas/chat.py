from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal, Optional
from llm import ModelID
from enum import Enum
from uuid import UUID, uuid4

class Role(str, Enum):
  USER = "user"
  ASSISTANT = "assistant"
  DEVELOPER = "developer"
  SYSTEM = "system"

class Message(BaseModel):
    """Schema for a message in the chat application."""
    
    role: Role = Field(
        description="The role of the message sender in the conversation."
    )
    content: str = Field(
        min_length=1,
        description="The content of the message."
    )

class UserMessage(Message):
    """Schema for a user message in the chat application."""
    
    role: Literal[Role.USER] = Field(     # constraint to ensure the role is always 'user'
        Role.USER,
        description="The role of the message sender in the conversation."
    )

class AssistantMessage(Message):
    """Schema for an assistant message in the chat application."""
    
    role: Literal[Role.ASSISTANT] = Field(     # constraint to ensure the role is always 'assistant'
        Role.ASSISTANT,
        description="The role of the message sender in the conversation."
    )

class Chat(BaseModel):
    """Schema for a chat message in the conversation."""
    
    id: int = Field(
        gt=0,
        description="Unique identifier for the chat message, typically an auto-incrementing integer."
    )
    conversation_id: UUID = Field(
        default_factory=uuid4,
        description="Identifier for the conversation this chat message belongs to."
    )
    message: Message = Field(
        description="The message content and role."
    )
    created_at: str = Field(
        default_factory=datetime.now,
        description="Timestamp when the chat message was created."
    )

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    
    conversation_id: Optional[UUID] = Field(
        default_factory=uuid4,
        description="The conversation ID to use for the chat completion"
    )
    message: UserMessage = Field(
        description="The message to send to the chat model"
    ) 
    model_id: str = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model to use for the chat completion"
    )

    class Config:
        """Configuration for ChatRequest model"""
        json_schema_extra = {
            "example": {
                "conversation_id": "22c4f8b-2d3e-4a5b-8c7f-1a2b3c4d5e6f",
                "message": {
                    "role": "user",
                    "content": "What is the meaning of life?",
                },
                "model_id": "openai_gpt-4o-mini",
            }
        }

class ChatResponse(BaseModel):
    """Response body for chat endpoint"""
    
    conversation_id: UUID = Field(
        default_factory=uuid4,
        description="The conversation ID used for the chat completion"
    )
    message: AssistantMessage = Field(
        description="The message returned by the chat model"
    )
    model_id: str = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model used for the chat completion"
    )

    class Config:
        """Configuration for ChatResponse model"""
        json_schema_extra = {
            "example": {
                "conversation_id": "22c4f8b-2d3e-4a5b-8c7f-1a2b3c4d5e6f",
                "message": {
                    "role": "assistant",
                    "content": "The meaning of life is subjective and can vary from person to person.",
                },
                "model_id": "openai_gpt-4o-mini",
            }
        }