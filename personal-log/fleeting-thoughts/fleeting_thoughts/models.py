"""Data models for the Fleeting Thoughts application.

This module defines the core data structures used throughout the application
using Pydantic models for data validation and serialization.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class Thought(BaseModel):
    """Represents a single thought entry with content and timestamp."""
    content: str = Field(..., description="The fleeting thought content")
    timestamp: datetime = Field(..., description="When the thought was recorded")

class DailyThoughts(BaseModel):
    """Collection of thoughts for a specific date."""
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="The date of these thoughts in YYYY-MM-DD format")
    thoughts: List[Thought] = Field(default_factory=list, description="List of thoughts for the day")