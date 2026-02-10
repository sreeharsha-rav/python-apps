import requests
import logging
from typing import ClassVar, List, Dict, Any
from src.search.engines.base_search import BaseSearch
from src.schemas.search import SearchEngineInfo, SearchEngineID, SearchResult
from src.config.settings import settings
from src.utils.decorators import singleton
from src.exceptions.search import SearchEngineConfigError, SearchQueryError


@singleton
class GoogleSearchAPI(BaseSearch):
    """Implementation of Google Custom Search API."""

    ENGINE_INFO: ClassVar[SearchEngineInfo] = SearchEngineInfo(
        engine_id=SearchEngineID.GOOGLE,
        name="Google Custom Search",
        max_results_per_query=10,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.logger = logging.getLogger(__name__)
            
            # Get credentials from settings
            self.api_key = settings.GOOGLE_CSE_API_KEY
            self.search_engine_id = settings.GOOGLE_CSE_ID
            self.base_url = "https://www.googleapis.com/customsearch/v1"

            # Validate required environment variables
            if not self.api_key:
                raise SearchEngineConfigError("GOOGLE_CSE_API_KEY environment variable is not set")
            if not self.search_engine_id:
                raise SearchEngineConfigError("GOOGLE_CSE_ID environment variable is not set")

            self._initialized = True

    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        self.logger.debug(f"Starting Google search with query: {query[:50]}...")
        
        if not query:
            raise SearchQueryError("Search query cannot be empty")

        num_results = min(num_results, self.ENGINE_INFO.max_results_per_query)
        self.logger.debug(f"Requesting {num_results} results")

        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'num': num_results
        }

        try:
            self.logger.debug("Sending request to Google API")
            response = requests.get(self.base_url, params=params, timeout=5)

            if response.status_code in (401, 403):
                raise SearchQueryError(f"Authentication error: {response.status_code}")
            elif response.status_code == 429:
                raise SearchQueryError("Rate limit exceeded for Google Search API")

            response.raise_for_status()
            results = response.json()

            if 'items' not in results:
                self.logger.debug("No search results found")
                return []

            self.logger.debug(f"Processing {len(results['items'])} search results")
            formatted_results = [
                SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', '')
                ) for item in results['items']
                if 'title' in item and 'link' in item and 'snippet' in item
            ]

            return formatted_results

        except requests.Timeout:
            raise SearchQueryError("Search request timed out")
        except requests.ConnectionError:
            raise SearchQueryError("Connection error during search")
        except requests.exceptions.RequestException as e:
            raise SearchQueryError(f"Search query failed: {str(e)}")