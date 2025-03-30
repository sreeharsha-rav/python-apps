from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter(
    prefix="/v1/conversation",
    tags=["conversation"],
)

class ConversationRequest(BaseModel):
    """A conversation with a chat model"""
    conversation_id: int = Field(gt=0, description="The conversation ID")
    title: Optional[str] = Field(description="The title of the conversation")

@router.get("")
def get_conversations():
    """Get all conversations"""
    return {"conversations": []}

@router.post("")
def create_conversation(conversation_request: ConversationRequest):
    """Create a new conversation"""
    return conversation_request.model_dump_json()

@router.get("/{conversation_id}")
def get_conversation(conversation_id: int):
    """Get a conversation by ID"""
    return {"conversation_id": conversation_id}

@router.put("/{conversation_id}")
def update_conversation(conversation_id: int, conversation_request: ConversationRequest):
    """Update a conversation by ID"""
    return conversation_request.model_dump_json()

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int):
    """Delete a conversation by ID"""
    return {"conversation_id": conversation_id}
