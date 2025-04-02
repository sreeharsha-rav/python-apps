from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class SearchEngineID(str, Enum):
    """Enum for supported search engine IDs"""
    GOOGLE = "google"
    # Add more search engines as you implement them
    # DUCKDUCKGO = "duckduckgo"
    # BING = "bing"

class SearchEngineInfo(BaseModel):
    """Information about the search engine"""
    engine_id: SearchEngineID = Field(description="Unique identifier for the search engine")
    name: str = Field(description="Display name for the search engine")
    max_results_per_query: int = Field(gt=0, description="Maximum number of results per query")

class SearchResult(BaseModel):
    """A single search result item from the search engine"""
    title: str = Field(description="Title of the search result")
    link: str = Field(description="URL of the search result")
    snippet: str = Field(description="Snippet or description of the search result")
    ## Add more fields as needed, like image URL, etc.

class AISearchResult(SearchResult):
    """AI-enhanced search result with additional fields"""
    summary: str = Field(description="Generated LLM summary of the web page content")
    ## Can add more fields like score, rank, etc. if needed

class WebRAGResponse(BaseModel):
    """Response model for web search results"""
    search_performed: bool = Field(description="Indicates if web search was performed")
    search_query: str = Field(description="Original search query")
    search_results: List[SearchResult] = Field(default=[], description="List of search result without AI summary")
    formatted_results: str = Field(default="", description="Formatted search results ready for LLM consumption")
    total_results: int = Field(description="Total number of results found")
    engine_id: SearchEngineID = Field(description="ID of the search engine used")