"""Manager module for handling thought operations.

This module provides the main business logic for managing thoughts,
including adding new thoughts and retrieving existing ones.
"""

from datetime import datetime
from typing import Optional, List

from .models import DailyThoughts, Thought
from .storage import JsonStorage

class ThoughtsManager:
    """Manages the operations for thoughts including creation and retrieval."""

    def __init__(self, storage_dir: str = "./entries"):
        """Initialize the thoughts manager.

        Args:
            storage_dir (str): Directory path for storing thought files
        """
        self.storage = JsonStorage(storage_dir)

    def add_thought(self, content: str) -> Thought:
        """Add a new thought with current timestamp.

        Args:
            content (str): The content of the thought

        Returns:
            Thought: The newly created thought object
        """
        now = datetime.now().replace(microsecond=0)
        date = now.date().isoformat()
        
        daily_thoughts = self.get_thoughts_for_date(date) or DailyThoughts(
            date=date,
            thoughts=[]
        )

        new_thought = Thought(
            content=content,
            timestamp=now
        )
        
        daily_thoughts.thoughts.append(new_thought)
        self.storage.save(daily_thoughts)
        return new_thought

    def get_thoughts_for_date(self, date: str) -> Optional[DailyThoughts]:
        """Retrieve all thoughts for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format

        Returns:
            Optional[DailyThoughts]: Collection of thoughts for the date if exists
        """
        return self.storage.load(date)

    def get_all_thoughts(self) -> List[DailyThoughts]:
        """Retrieve all thoughts from all dates.

        Returns:
            List[DailyThoughts]: List of all thoughts grouped by date
        """
        files = list(self.storage.storage_dir.glob("*.json"))
        thoughts = []
        
        for file in files:
            date = file.stem
            daily_thoughts = self.get_thoughts_for_date(date)
            if (daily_thoughts):
                thoughts.append(daily_thoughts)
                
        return thoughts