from pathlib import Path
import json
from typing import List, Dict
from journal_bot.core.journal_entry import JournalEntry


class JsonStorage:
    def __init__(self):
        self.base_path = Path.home() / "journal_entries"
        self.base_path.mkdir(exist_ok=True)

    def save_entry(self, entry: JournalEntry) -> None:
        """Save a journal entry to JSON file"""
        date_str = entry.date.strftime("%Y-%m-%d_%H-%M-%S")
        file_path = self.base_path / f"entry_{date_str}.json"

        with open(file_path, "w") as f:
            json.dump(entry.model_dump(), f, indent=2, default=str)

    def list_entries(self) -> List[Dict]:
        """List all journal entries"""
        entries = []
        for file_path in self.base_path.glob("entry_*.json"):
            with open(file_path) as f:
                entries.append(json.load(f))
        return sorted(entries, key=lambda x: x["date"], reverse=True)
