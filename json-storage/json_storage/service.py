import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

class JSONFileManager:
    """Manages CRUD operations for JSON files with proper error handling"""
    
    def __init__(self, storage_dir: str = "./data"):
        """Initialize JSONFileManager with storage directory.
        
        Args:
          storage_dir (str): Directory to store JSON files (default: './data')
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def get_storage_dir(self) -> Path:
        """Get the storage directory path

        Returns:
          Path: Path object of the storage directory
        """
        return self.storage_dir

    def get_filename(self, date: Optional[date] = None) -> Path:
        """
        Generate filename for the specified date.
        
        Args:
            date (date, optional): Date for the file (default: None) in YYYY_MM_DD format
            
        Returns:
            Path: Complete filename path
        """
        if date is None:
            date = datetime.now().date()
        return f"{date.strftime('%Y_%m_%d')}.json"
    
    def file_exists(self, date: Optional[date] = None) -> bool:
        """
        Check if a file exists for the specified date.
        
        Args:
            date (date, optional): Date to check. Defaults to current date.
            
        Returns:
            bool: True if file exists, False otherwise
        """
        path = self.storage_dir / self.get_filename(date)
        return path.exists()

    def read_data(self, date: Optional[date] = None) -> Dict:
        """
        Read all data from a specific date's file.
        
        Args:
            date (date, optional): Date to read from. Defaults to current date.
            
        Returns:
            dict: Data from the JSON file or empty dict if file doesn't exist
        """
        filepath = self.storage_dir / self.get_filename(date)
        try:
            with filepath.open('r') as f:
                return json.load(f)
        except FileNotFoundError: # TODO: throw error global
            print("File not found")
            return {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {filepath}: {str(e)}")
    
    def write_data(self, data: Dict, date: Optional[date] = None) -> None:
        """
        Write complete data to a specific date's file. Generates a file if it does not exist.
        
        Args:
            data (dict): Data to write to the file
            date (date, optional): Date to write to. Defaults to current date.
        """
        filepath = self.storage_dir / self.get_filename(date)

        with filepath.open('w') as f:
            json.dump(data, f, indent=2)
    
    def update_data(self, key: str, value: Any, date: Optional[date] = None) -> None:
        """
        Update or add a specific key-value pair in the JSON file.
        
        Args:
            key (str): Key to update
            value (Any): Value to set
            date (date, optional): Date of file to update. Defaults to current date.
        """
        data = self.read_data(date)
        data[key] = value
        self.write_data(data, date)
    
    def append_to_list(self, key: str, value: Any, date: Optional[date] = None) -> None:
        """
        Append a value to a list at the specified key. Creates list if it doesn't exist.
        
        Args:
            key (str): Key where list is stored
            value (Any): Value to append to the list
            date (datetime, optional): Date of file to update. Defaults to current date.
        """
        data = self.read_data(date)
        if key not in data:
            data[key] = []
        if not isinstance(data[key], list):
            raise ValueError(f"Key '{key}' exists but is not a list")
        data[key].append(value)
        self.write_data(data, date)
    
    def delete_key(self, key: str, date: Optional[date] = None) -> bool:
        """
        Delete a key from the JSON file.
        
        Args:
            key (str): Key to delete
            date (datetime, optional): Date of file to update. Defaults to current date.
            
        Returns:
            bool: True if key was deleted, False if key didn't exist
        """
        data = self.read_data(date)
        if key in data:
            del data[key]
            self.write_data(data, date)
            return True
        return False
    
    def get_all_dates(self) -> List[date]:
        """
        Get list of all dates that have JSON files.
        
        Returns:
            List[datetime]: List of dates with existing files
        """
        dates = []
        for file in self.base_directory.glob("*.json"):
            try:
                date_str = file.stem  # Get filename without extension
                dates.append(date.fromisoformat(date_str))
            except ValueError:
                continue
        return sorted(dates)

class JSONFileError(Exception):
    """Custom exception for JSON file operations"""
    pass
