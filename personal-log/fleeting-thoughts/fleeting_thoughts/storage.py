"""Storage module for persisting thoughts data.

This module handles the JSON file storage operations for thoughts,
including saving and loading thought data from the filesystem.
"""

import json
from pathlib import Path
from typing import Optional

from .models import DailyThoughts

class JsonStorage:
    """Handles JSON file storage operations for thoughts."""

    def __init__(self, storage_dir: str = "./thoughts"):
        """Initialize the JSON storage.

        Args:
            storage_dir (str): Directory path for storing JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, date: str) -> Path:
        """Get the file path for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format

        Returns:
            Path: Path object for the JSON file
        """
        return self.storage_dir / f"{date}.json"

    def save(self, daily_thoughts: DailyThoughts) -> None:
        """Save daily thoughts to a JSON file.

        Args:
            daily_thoughts (DailyThoughts): Thoughts to save
        """
        file_path = self._get_file_path(daily_thoughts.date)
        with file_path.open("w") as f:
            json.dump(daily_thoughts.model_dump(), f, indent=2, default=str)

    def load(self, date: str) -> Optional[DailyThoughts]:
        """Load daily thoughts from a JSON file.

        Args:
            date (str): Date in YYYY-MM-DD format

        Returns:
            Optional[DailyThoughts]: Loaded thoughts if file exists
        """
        file_path = self._get_file_path(date)
        if not file_path.exists():
            return None
        
        with file_path.open("r") as f:
            data = json.load(f)
            return DailyThoughts.model_validate(data)