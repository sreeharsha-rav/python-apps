from src.prompts.search import USE_SEARCH_RESULTS, USER_SEARCH_QUERY
from src.schemas.chat import Chat, ChatRequest, ChatResponse, UserMessage, Role
from src.schemas.search import WebRAGResponse
from src.llm.llm_registry import LLMRegistry
from src.services.web_rag import WebRAGService
from src.repositories.chat import ChatRepository
from src.exceptions.chat import ChatNotFoundError
from src.prompts.chat import GENERAL_CHAT_PROMPT

# search
from src.schemas.search import SearchEngineID

from ulid import ULID
from typing import List
import logging

class ChatService:
    def __init__(self):
        self._llm_registry = LLMRegistry()
        self._chat_repository = ChatRepository()
        self._web_rag_service = WebRAGService()
        self.logger = logging.getLogger(__name__)

    async def generate_chat_completion(self, chat_request: ChatRequest) -> ChatResponse:
        """Generate a chat completion from a user message."""
        self.logger.debug(f"Starting chat completion for chat_id={chat_request.chat_id}")
        
        llm = self._llm_registry.get_model(chat_request.model_id)
        self.logger.debug(f"Using LLM model: {chat_request.model_id}")
        
        chat_exists = await self._chat_repository.chat_exists(chat_request.chat_id)
        self.logger.debug(f"Chat exists: {chat_exists}")

        self.logger.debug("Executing Web RAG process")
        rag_response = await self._web_rag_service.execute_web_rag(
            user_message=chat_request.message,
            llm=llm,
            engine_id=SearchEngineID.GOOGLE
        )

        self.logger.debug(f"Web search performed: {rag_response.search_performed}")
        if rag_response.search_performed and rag_response.search_results:
            system_prompt = USE_SEARCH_RESULTS
            self.logger.debug("Using search-based system prompt")
            message_with_web_rag_context = UserMessage(
                role=Role.USER,
                content=USER_SEARCH_QUERY.format(
                    search_query=rag_response.search_query,
                    formatted_results=rag_response.formatted_results
                )
            )
        else:
            system_prompt = GENERAL_CHAT_PROMPT
            self.logger.debug("Using general system prompt")
            message_with_web_rag_context = UserMessage(
                role=Role.USER,
                content=chat_request.message.content
            )

        if chat_exists:
            self.logger.debug("Updating existing chat")
            existing_chat = await self._chat_repository.get(chat_request.chat_id)
            self.logger.debug("Generating completion with chat history")
            assistant_message = await llm.get_completion(
                system_instruction=system_prompt,
                messages=existing_chat.messages + [message_with_web_rag_context]
            )
            existing_chat.messages.extend([chat_request.message, assistant_message])
            await self._chat_repository.update_messages(
                chat_id=chat_request.chat_id,
                messages=existing_chat.messages
            )
        else:
            self.logger.debug("Creating new chat")
            assistant_message = await llm.get_completion(
                system_instruction=system_prompt,
                messages=[message_with_web_rag_context]
            )
            chat_history = [chat_request.message, assistant_message]
            new_chat = Chat(
                chat_id=chat_request.chat_id,
                title=chat_request.message.content,
                messages=chat_history,
            )
            await self._chat_repository.create(new_chat)

        self.logger.debug("Completing chat generation")
        return ChatResponse(
            chat_id=chat_request.chat_id,
            message=assistant_message,
            model_id=chat_request.model_id,
            web_search=rag_response.search_performed,
            search_results=rag_response.search_results
        )

    async def get_chat(self, chat_id: ULID) -> Chat:
        """Retrieve a chat by its ID."""
        chat = await self._chat_repository.get(chat_id)
        if chat is None:
            raise ChatNotFoundError(f"Chat with ID {chat_id} not found")
        return chat

    async def list_chats(self) -> List[Chat]:
        """Retrieve all chats."""
        return await self._chat_repository.list()

    async def delete_chat(self, chat_id: ULID) -> None:
        """Delete a chat by its ID."""
        await self._chat_repository.delete(chat_id)
