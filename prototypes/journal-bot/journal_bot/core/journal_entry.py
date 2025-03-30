from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class JournalEntry(BaseModel):
    date: datetime = Field(default_factory=datetime.now)
    opening_reflection: Dict[str, str]
    modules: Dict[str, Dict[str, str]]
    closing_integration: Dict[str, str]

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2023-12-20T20:30:00Z",
                "opening_reflection": {
                    "prompt": "In this moment, I notice...",
                    "response": "a sense of calm and focus",
                },
            }
        }
