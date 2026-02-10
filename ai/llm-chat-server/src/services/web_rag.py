import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional
from src.prompts.search import SHOULD_USE_WEB_SEARCH, GENERATE_SEARCH_QUERY, SUMMARIZE_WEB_CONTENT
from src.llm.models.base_llm import BaseLLM
from src.schemas.search import SearchEngineID, SearchResult, AISearchResult, WebRAGResponse
from src.schemas.chat import UserMessage, AssistantMessage
from src.search.search_registry import SearchRegistry

TRUNCATE_SCRAPED_TEXT = 10000  # adjust based on Model's context window
CHARACTER_LIMIT = 1000  # adjust for tokenization considerations

class WebRAGService:
    """Web Retrieval-Augmented Generation (RAG) service for handling web searches and content summarization."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._search_registry = SearchRegistry()

    async def perform_web_search(self, user_message: UserMessage, llm: BaseLLM, engine_id: SearchEngineID = SearchEngineID.GOOGLE) -> List[SearchResult]:
        """
        Perform a web search based on the user's message.

        Args:
            user_message: The user's message
            llm: The language model instance
            engine_id: The search engine ID

        Returns:
            List[SearchResult]: A list of search results
        """
        self.logger.debug("Generating search query from user message")
        search_query: AssistantMessage = await llm.get_completion(
            system_instruction=GENERATE_SEARCH_QUERY,
            messages=[user_message]
        )
        self.logger.debug(f"Generated search query: {search_query.content}")
        
        self.logger.debug(f"Executing search with engine: {engine_id}")
        search_engine = self._search_registry.get_engine(engine_id)
        return search_engine.search(
            query=search_query.content,
            num_results=5
        )

    async def retrieve_content(self, url: str) -> Optional[str]:
        """
        Retrieve content from a given URL.

        Args:
            url: The URL to retrieve content from

        Returns:
            Optional[str]: The retrieved content or None if retrieval fails
        """
        self.logger.debug(f"Retrieving content from URL: {url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            self.logger.debug("Parsing and cleaning content")
            soup = BeautifulSoup(response.content, 'html.parser')
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            content = '\n'.join(lines)

            max_content_length = TRUNCATE_SCRAPED_TEXT * 4
            if len(content) > max_content_length:
                self.logger.debug(f"Content truncated from {len(content)} to {max_content_length} characters")
                content = content[:max_content_length] + "..."

            return content
        except Exception as e:
            self.logger.error(f"Failed to retrieve content from {url}: {str(e)}")
            return None

    async def summarize_content(self, content: str, query: str, llm: BaseLLM) -> str:
        if not content:
            return "No content available for summarization."

        system_prompt = SUMMARIZE_WEB_CONTENT.format(
            search_query=query,
            character_limit=CHARACTER_LIMIT,
        )
        
        user_message = UserMessage(content=f"search_query: {query}\nweb_page_content:{content}")
        summary_response: AssistantMessage = await llm.get_completion(
            system_instruction=system_prompt,
            messages=[user_message]
        )

        return summary_response.content

    async def build_search_context(self, search_results: List[SearchResult], search_query: str, llm: BaseLLM) -> List[AISearchResult]:
        """
        Build a search context by retrieving and summarizing content from search results.

        Args:
            search_results: List of search results from `perform_web_search()`
            search_query: The original search query (not the generated one)
            llm: The language model instance

        Returns:
            List[AISearchResult]: A list of AI-enhanced search results with summaries
        """
        ai_search_results: List[AISearchResult] = []

        for result in search_results:
            # Retrieve content from the link
            self.logger.info(f"Retrieving content from: {result.link}")
            content = await self.retrieve_content(result.link)

            # create ai_search_result object
            ai_search_result = AISearchResult(
                title=result.title,
                link=result.link,
                snippet=result.snippet,
                summary="",         # placeholder for now
            )

            # get summary of the content if available
            if content:
                self.logger.info(f"Summarizing content for: {result.link}")
                summary = await self.summarize_content(content, search_query, llm)
                ai_search_result.summary = summary

            # add the ai_search_result to the list
            ai_search_results.append(ai_search_result)

        return ai_search_results

    async def execute_web_rag(self, user_message: UserMessage, llm: BaseLLM, engine_id: SearchEngineID = SearchEngineID.GOOGLE):
        """
        Execute the Web Retrieval-Augmented Generation (RAG) process.

        Args:
            user_message: The user's message
            llm: The language model instance
            engine_id: The search engine ID

        Returns:
            WebRAGResponse: The response containing search results and formatted results
        """
        self.logger.debug("Starting Web RAG execution")
        rag_response = WebRAGResponse(
            search_performed=False,
            search_query=user_message.content,
            search_results=[],
            formatted_results="",
            total_results=0,
            engine_id=engine_id
        )

        self.logger.debug("Checking if web search is needed")
        should_use_web_search = await llm.get_completion(
            system_instruction=SHOULD_USE_WEB_SEARCH,
            messages=[user_message]
        )

        if should_use_web_search.content == "true":
            self.logger.debug("Web search needed, performing search")
            search_results = await self.perform_web_search(
                user_message=user_message,
                llm=llm,
                engine_id=engine_id
            )

            self.logger.debug("Building search context")
            ai_search_results = await self.build_search_context(
                search_results=search_results,
                search_query=user_message.content,
                llm=llm
            )

            self.logger.debug("Formatting search results")
            formatted_results = ""
            for i, result in enumerate(ai_search_results, 1):
                formatted_results += f"[Source {i}] {result.title}\n"
                formatted_results += f"URL: {result.link}\n"
                formatted_results += f"Summary: {result.summary}\n\n"

            rag_response.search_performed = True
            rag_response.search_results = search_results
            rag_response.formatted_results = formatted_results
            rag_response.total_results = len(search_results)
        else:
            self.logger.debug("Web search not needed")

        return rag_response