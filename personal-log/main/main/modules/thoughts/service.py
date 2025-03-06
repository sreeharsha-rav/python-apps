from datetime import date
from typing import Optional, List

from main.modules.thoughts.model import Thought, Thoughts
from main.storage.json_file_manager import JSONFileManager

class ThoughtsService:
    """Service for managing fleeting thoughts entries"""
    
    KEY = "fleeting_thoughts"
    
    def __init__(self, file_manager: JSONFileManager):
        """
        Initialize the service with a file manager
        
        Args:
            file_manager (JSONFileManager): JSON file manager for storage operations
        """
        self.file_manager = file_manager
    
    def get_thoughts(self, entry_date: Optional[date] = None) -> Thoughts:
        """
        Get thoughts for a specific date
        
        Args:
            entry_date (date, optional): Date to retrieve thoughts for. Defaults to current date.
            
        Returns:
            Thoughts: Thoughts model with data for the specified date
        """
        data = self.file_manager.read_data(entry_date)
        if self.KEY not in data:
            return Thoughts()
            
        return Thoughts.model_validate(data[self.KEY])
    
    def add_thought(self, thought: Thought, entry_date: Optional[date] = None) -> None:
        """
        Add a single thought to the specified date
        
        Args:
            thought (Thought): Thought to add
            entry_date (date, optional): Date to add the thought to. Defaults to current date.
        """
        # check if the date exists
        if not self.file_manager.file_exists(entry_date):
            self.file_manager.write_data({self.KEY: Thoughts().model_dump(exclude_none=True, mode='json')}, entry_date)

        # Get existing thoughts
        existing_thoughts = self.get_thoughts(entry_date)
        
        # Add new thought
        existing_thoughts.thoughts.append(thought)
        
        # Update file
        data = self.file_manager.read_data(entry_date)
        # Use model_dump with exclude_none=True and serialize datetime objects
        data[self.KEY] = existing_thoughts.model_dump(exclude_none=True, mode='json')
        self.file_manager.write_data(data, entry_date)
    
    def save_thoughts(self, thoughts: Thoughts, entry_date: Optional[date] = None) -> None:
        """
        Save all thoughts for a date
        
        Args:
            thoughts (Thoughts): Thoughts to save
            entry_date (date, optional): Date to save thoughts for. Defaults to current date.
        """
        data = self.file_manager.read_data(entry_date)
        data[self.KEY] = thoughts.model_dump(exclude_none=True, mode='json')
        self.file_manager.write_data(data, entry_date)