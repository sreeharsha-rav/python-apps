from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Conversation(BaseModel):
    """Schema for a conversation in the chat application."""
    
    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the conversation, typically a UUID."
    )
    title: str = Field(
        description="Title of the conversation."
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the conversation was created."
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp when the conversation was last updated."
    )