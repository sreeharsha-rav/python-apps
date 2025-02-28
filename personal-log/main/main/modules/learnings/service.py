from datetime import date
from typing import Optional, List

from main.modules.learnings.model import Learning, LearningEntry
from main.storage.json_file_manager import JSONFileManager

class LearningsService:
    """Service for managing learning entries"""
    
    KEY = "learnings"
    
    def __init__(self, file_manager: JSONFileManager):
        """Initialize the service with a file manager
        
        Args:
            file_manager (JSONFileManager): JSON file manager for storage operations
        """
        self.file_manager = file_manager
    
    def get_learnings(self, entry_date: Optional[date] = None) -> LearningEntry:
        """Get learnings for a specific date
        
        Args:
            entry_date (date, optional): Date to retrieve learnings for. Defaults to current date.
            
        Returns:
            LearningEntry: LearningEntry model with data for the specified date
        """
        data = self.file_manager.read_data(entry_date)
        if self.KEY not in data:
            return LearningEntry()
            
        return LearningEntry.model_validate(data[self.KEY])
    
    def add_learning(self, learning: Learning, entry_date: Optional[date] = None) -> None:
        """Add a single learning to the specified date
        
        Args:
            learning (Learning): Learning to add
            entry_date (date, optional): Date to add the learning to. Defaults to current date.
        """
        # Get existing learnings
        existing_learnings = self.get_learnings(entry_date)
        
        # Add new learning
        existing_learnings.learnings.append(learning)
        
        # Update file
        data = self.file_manager.read_data(entry_date)
        data[self.KEY] = existing_learnings.model_dump()
        self.file_manager.write_data(data, entry_date)
    
    def save_learnings(self, learnings: LearningEntry, entry_date: Optional[date] = None) -> None:
        """Save all learnings for a date
        
        Args:
            learnings (LearningEntry): Learnings to save
            entry_date (date, optional): Date to save learnings for. Defaults to current date.
        """
        data = self.file_manager.read_data(entry_date)
        data[self.KEY] = learnings.model_dump()
        self.file_manager.write_data(data, entry_date)