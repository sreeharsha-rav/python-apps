from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    id: str = Field(default_factory=lambda: f"todo-{uuid4()}")
    title: str = Field(min_length=1, max_length=255, description="The title of the todo item")
    description: str = Field(min_length=1, max_length=1024, description="A detailed description of the todo item")
    completed: bool = Field(default=False, description="Whether the todo item is completed or not")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="The timestamp when the todo item was created")
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="The timestamp when the todo item was last updated")

    model_config = {
        "strip_whitespace": True
    }
