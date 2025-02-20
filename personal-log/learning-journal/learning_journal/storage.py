import json
from pathlib import Path
from .models import LearningEntry

class JsonStorage:
    """Handles JSON file storage operations for learning journal entries."""

    def __init__(self, storage_dir: str = "./entries"):
        """Initialize the JSON storage.

        Args:
            storage_dir (str): Directory path for storing JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, entry_date: str) -> Path:
        """Get the file path for a specific date.

        Args:
            entry_date(str): Date in YYYY-MM-DD format

        Returns:
            Path: Path object for the JSON file
        """
        return self.storage_dir / f"{entry_date}.json"
    
    def save_entry(self, entry: LearningEntry) -> None:
        """Save learning entry to a JSON file.

        Args:
            entry (LearningEntry): Entry to save
        """
        file_path = self._get_file_path(entry.date)
        with open(file_path, 'w') as f:
            json.dump(entry.model_dump(), f, indent=2, default=str)
    
    def load_entry(self, entry_date: str) -> LearningEntry:
        """Load learning entry from a JSON file.

        Args:
            entry_date (str): Date in YYYY-MM-DD format

        Returns:
            LearningEntry: Loaded entry if file exists
        """
        file_path = self._get_file_path(entry_date)
        if not file_path.exists():
            return None
            
        with open(file_path) as f:
            data = json.load(f)
            return LearningEntry.model_validate(data)
