from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class Thought(BaseModel):
    """Represents a single thought entry with content and timestamp."""
    content: str = Field(..., description="The fleeting thought content")
    timestamp: datetime = Field(..., description="When the thought was recorded")

class Thoughts(BaseModel):
    """Collection of thoughts for the day."""
    thoughts: List[Thought] = Field(default_factory=list, description="List of thoughts for the day")