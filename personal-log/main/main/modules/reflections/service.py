from datetime import date
from typing import Optional, List

from main.modules.reflections.model import Reflection, LearningReflections
from main.storage.json_file_manager import JSONFileManager

class ReflectionsService:
    """Service for managing daily reflections"""
    
    KEY = "reflections"
    
    def __init__(self, file_manager: JSONFileManager):
        """Initialize the service with a file manager
        
        Args:
            file_manager (JSONFileManager): JSON file manager for storage operations
        """
        self.file_manager = file_manager
    
    def get_reflection(self, entry_date: Optional[date] = None) -> Optional[Reflection]:
        """Get reflection for a specific date
        
        Args:
            entry_date (date, optional): Date to retrieve reflection for. Defaults to current date.
            
        Returns:
            Optional[Reflection]: Reflection model if exists, None otherwise
        """
        data = self.file_manager.read_data(entry_date)
        if self.KEY not in data:
            return None
            
        return Reflection.model_validate(data[self.KEY])
    
    def save_reflection(self, reflection: Reflection, entry_date: Optional[date] = None) -> None:
        """Save reflection for a date
        
        Args:
            reflection (Reflection): Reflection to save
            entry_date (date, optional): Date to save reflection for. Defaults to current date.
        """
        # Ensure file exists
        if not self.file_manager.file_exists(entry_date):
            self.file_manager.write_data({}, entry_date)
        
        # Get existing data and update with new reflection
        data = self.file_manager.read_data(entry_date)
        data[self.KEY] = reflection.model_dump(exclude_none=True, by_alias=True)
        
        # Write updated data back to file
        self.file_manager.write_data(data, entry_date)
    
    def update_thoughts_reflection(self, reflection_text: str, entry_date: Optional[date] = None) -> None:
        """Update just the thoughts reflection component
        
        Args:
            reflection_text (str): New reflection text
            entry_date (date, optional): Date to update. Defaults to current date.
        """
        reflection = self.get_reflection(entry_date)
        if not reflection:
            reflection = Reflection(thoughts_reflections=reflection_text)
        else:
            reflection.thoughts_reflections = reflection_text
            
        self.save_reflection(reflection, entry_date)
    
    def update_learning_reflection(self, key_takeaways: List[str], action_items: List[str], entry_date: Optional[date] = None) -> None:
        """Update the learning reflection component
        
        Args:
            key_takeaways (List[str]): List of main learnings and insights
            action_items (List[str]): List of next steps or areas to explore
            entry_date (date, optional): Date to update. Defaults to current date.
        """
        reflection = self.get_reflection(entry_date)
        learning_reflection = LearningReflections(
            key_takeaways = key_takeaways,
            action_items = action_items
        )
        
        if not reflection:
            reflection = Reflection(learning_reflections=learning_reflection)
        else:
            reflection.learning_reflections = learning_reflection
            
        self.save_reflection(reflection, entry_date)
    
    def add_key_takeaway(self, takeaway: str, entry_date: Optional[date] = None) -> None:
        """Add a single key takeaway to the learning reflection
        
        Args:
            takeaway (str): Key takeaway to add
            entry_date (date, optional): Date to update. Defaults to current date.
        """
        reflection = self.get_reflection(entry_date)
        
        if not reflection:
            # Create new reflection with this takeaway
            learning_reflection = LearningReflections(key_takeaways=[takeaway])
            reflection = Reflection(learning_reflections=learning_reflection)
        elif not reflection.learning_reflections:
            # Create new learning reflection with this takeaway
            reflection.learning_reflections = LearningReflections(key_takeaways=[takeaway])
        else:
            # Add to existing takeaways
            reflection.learning_reflections.key_takeaways.append(takeaway)
        
        self.save_reflection(reflection, entry_date)
    
    def add_action_item(self, action: str, entry_date: Optional[date] = None) -> None:
        """Add a single action item to the learning reflection
        
        Args:
            action (str): Action item to add
            entry_date (date, optional): Date to update. Defaults to current date.
        """
        reflection = self.get_reflection(entry_date)
        
        if not reflection:
            # Create new reflection with this action
            learning_reflection = LearningReflections(action_items=[action])
            reflection = Reflection(learning_reflections=learning_reflection)
        elif not reflection.learning_reflections:
            # Create new learning reflection with this action
            reflection.learning_reflections = LearningReflections(action_items=[action])
        else:
            # Add to existing actions
            reflection.learning_reflections.action_items.append(action)
        
        self.save_reflection(reflection, entry_date)