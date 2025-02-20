from datetime import date
from typing import Optional, List
from rich.prompt import Prompt, Confirm
from .models import Learning, LearningEntry
from .storage import JsonStorage

class JournalManager:
    """Manages learning journal operations."""
    
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def add_entry(self, entry_date: date) -> None:
        """Add a new journal entry with user prompts."""
        learnings = []
        
        while True:
            topic = Prompt.ask("Enter topic")
            insight = Prompt.ask("What did you learn?")
            connection = Prompt.ask(
                "How does this connect to what you know? (optional)",
                default=""
            )
            
            learning = Learning(
                topic=topic,
                insight=insight,
                connection=connection if connection else None
            )
            learnings.append(learning)
            
            if not Confirm.ask("Add another learning?"):
                break
        
        entry = LearningEntry(
            date=str(entry_date),
            learnings=learnings
        )
        self.storage.save_entry(entry)

    def get_entry(self, entry_date: date) -> Optional[LearningEntry]:
        """Get entry for a specific date."""
        return self.storage.load_entry(str(entry_date))