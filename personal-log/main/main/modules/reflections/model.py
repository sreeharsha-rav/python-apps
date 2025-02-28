from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class LearningReflections(BaseModel):
    """Model for learning reflections component."""
    model_config = ConfigDict(populate_by_name=True)
    
    key_takeaways: List[str] = Field(
        default_factory=list,
        alias="keyTakeaways",
        description="Main learnings and insights from the day"
    )
    action_items: List[str] = Field(
        default_factory=list,
        alias="actionItems",
        description="Actionable items or next steps"
    )

class Reflection(BaseModel):
    """Model for the reflection component of daily entries."""
    thoughts_reflections: Optional[str] = Field(None, description="Brief summary of fleeting thoughts and observations")
    learning_reflections: Optional[LearningReflections] = Field(None, description="Reflections on learnings from the day")