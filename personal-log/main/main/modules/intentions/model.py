from typing import List, Optional
from pydantic import BaseModel, Field

class Priority(BaseModel):
    """Represents a single priority item with task and alignment."""
    task: str = Field(..., description="Task description")
    alignment: str = Field(..., description="How task aligns with goals")

class Intentions(BaseModel):
    """Represents the intentions component of the daily entry."""
    long_term_goals: List[str] = Field(..., description="Long-term goals")
    short_term_goals: List[str] = Field(..., description="Short-term goals")
    affirmation: Optional[str] = Field(None, description="Positive affirmation for the day, optional")

class DailyIntentions(BaseModel):
    """Collection of intentions and priorities for a day."""
    intentions: Intentions = Field(..., description="Intentions for the day")
    priorities: List[Priority] = Field(..., min_items=1, max_items=3, description="List of priorities for the day")