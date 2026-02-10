from fastapi import APIRouter, status, HTTPException, Path
from typing import List
import logging
from src.services.chat import ChatService
from src.schemas.chat import Chat, ChatRequest, ChatResponse
from src.exceptions.chat import ChatNotFoundError
from ulid import ULID
import time

router = APIRouter(
    prefix="/v1/chat",
    tags=["chat"],
)

logger = logging.getLogger(__name__)
chat_service = ChatService()

@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(chat_request: ChatRequest) -> ChatResponse:
    """Create a chat from a user message"""
    logger.debug(f"Received chat creation request for chat_id={chat_request.chat_id}")
    start_time = time.time()
    try:
        response = await chat_service.generate_chat_completion(chat_request)
        logger.info(f"Chat completion processed in {(time.time() - start_time) * 1000:.2f}ms")
        return response
    except Exception as e:
        logger.error(f"Failed to process chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chat_id}", response_model=Chat)
async def get_chat(chat_id: ULID = Path(description="The chat ID to get")) -> Chat:
    logger.debug(f"Fetching chat with ID: {chat_id}")
    try:
        return await chat_service.get_chat(chat_id)
    except ChatNotFoundError:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found")

@router.get("", response_model=List[Chat])
async def list_chats() -> List[Chat]:
    logger.debug("Fetching all chats")
    return await chat_service.list_chats()

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: ULID = Path(description="The chat ID to delete")) -> None:
    logger.debug(f"Deleting chat with ID: {chat_id}")
    await chat_service.delete_chat(chat_id)