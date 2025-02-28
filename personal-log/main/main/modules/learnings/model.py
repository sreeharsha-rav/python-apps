from typing import List, Optional
from pydantic import BaseModel, Field

class Learning(BaseModel):
    """
    Learning model to represent a learning journal entry.

    Attributes:
        topic (str): Brief topic or context of the learning.
        insight (str): Description of what was learned.
        connection (Optional[str]): Explanation of how the learning connects to existing knowledge or how it can be applied.
    """
    topic: str = Field(..., description="Brief topic or context")
    insight: str = Field(..., description="What was learned")
    connection: Optional[str] = Field(None, description="How it connects to existing knowledge or how to apply it")

class LearningEntry(BaseModel):
    """
    LearningEntry model to represent a daily learning journal entry.

    Attributes:
        learnings (List[Learning]): List of learnings for the day.
    """
    learnings: List[Learning] = Field(default_factory=list, description="List of learnings for the day")

