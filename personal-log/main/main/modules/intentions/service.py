from datetime import date
from typing import Optional

from main.modules.intentions.model import DailyIntentions
from main.storage.json_file_manager import JSONFileManager

class IntentionsService:
    """Service for managing intentions entries"""
    
    KEY = "daily_intentions"
    
    def __init__(self, file_manager: JSONFileManager):
        """
        Initialize the service with a file manager
        
        Args:
            file_manager (JSONFileManager): JSON file manager for storage operations
        """
        self.file_manager = file_manager
    
    def get_daily_intentions(self, entry_date: Optional[date] = None) -> Optional[DailyIntentions]:
        """
        Get daily intentions for a specific date
        
        Args:
            entry_date (date, optional): Date to retrieve intentions for. Defaults to current date.
            
        Returns:
            Optional[DailyIntentions]: DailyIntentions model if exists, None otherwise
        """
        data = self.file_manager.read_data(entry_date)
        if self.KEY not in data:
            return None
            
        return DailyIntentions.model_validate(data[self.KEY])
    
    def save_daily_intentions(self, daily_intentions: DailyIntentions, entry_date: Optional[date] = None) -> None:
        """
        Save daily intentions for a date
        
        Args:
            daily_intentions (DailyIntentions): Intentions to save
            entry_date (date, optional): Date to save intentions for. Defaults to current date.
        """
        data = self.file_manager.read_data(entry_date)
        data[self.KEY] = daily_intentions.model_dump(by_alias=True)
        self.file_manager.write_data(data, entry_date)
    
    def update_affirmation(self, affirmation: str, entry_date: Optional[date] = None) -> None:
        """
        Update just the affirmation in the daily intentions
        
        Args:
            affirmation (str): New affirmation text
            entry_date (date, optional): Date to update. Defaults to current date.
        """
        daily_intentions = self.get_daily_intentions(entry_date)
        if daily_intentions:
            daily_intentions.intentions.affirmation = affirmation
            self.save_daily_intentions(daily_intentions, entry_date)