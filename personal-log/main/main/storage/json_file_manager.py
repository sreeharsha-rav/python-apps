import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to serialize datetime and date objects"""

    def default(self, obj):
        """Override default method to handle datetime and date objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class JSONFileError(Exception):
    """Custom exception for JSON file operations"""
    pass

class JSONFileManager:
    """Manages CRUD operations for JSON files with proper error handling"""
    
    def __init__(self, storage_dir: str = "./data"):
        """Initialize JSONFileManager with storage directory.
        
        Args:
            storage_dir (str): Directory to store JSON files (default: './data')
            
        Raises:
            JSONFileError: If the storage directory cannot be created
        """
        self.storage_dir = Path(storage_dir)
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise JSONFileError(f"Permission denied: Cannot create storage directory at {storage_dir}")
        except OSError as e:
            raise JSONFileError(f"Failed to create storage directory at {storage_dir}: {str(e)}")
    
    def get_storage_dir(self) -> Path:
        """Get the storage directory path

        Returns:
            Path: Path object of the storage directory
        """
        return self.storage_dir

    def get_filename(self, date_obj: Optional[date] = None) -> str:
        """
        Generate filename for the specified date.
        
        Args:
            date_obj (date, optional): Date for the file (default: None) in YYYY_MM_DD format
            
        Returns:
            str: Filename string (not full path)
        """
        if date_obj is None:
            date_obj = datetime.now().date()
        return f"{date_obj.strftime('%Y_%m_%d')}.json"
    
    def file_exists(self, date_obj: Optional[date] = None) -> bool:
        """
        Check if a file exists for the specified date.
        
        Args:
            date_obj (date, optional): Date to check. Defaults to current date.
            
        Returns:
            bool: True if file exists, False otherwise
        """
        path = self.storage_dir / self.get_filename(date_obj)
        return path.exists()

    def read_data(self, date_obj: Optional[date] = None) -> Dict:
        """
        Read all data from a specific date's file.
        
        Args:
            date_obj (date, optional): Date to read from. Defaults to current date.
            
        Returns:
            dict: Data from the JSON file or empty dict if file doesn't exist
            
        Raises:
            JSONFileError: If there's an error reading the file (other than not found)
        """
        filepath = self.storage_dir / self.get_filename(date_obj)
        try:
            with filepath.open('r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            # Back up corrupted file
            backup_path = filepath.with_suffix('.json.bak')
            try:
                filepath.rename(backup_path)
                error_msg = f"Corrupted JSON file at {filepath}. Backed up to {backup_path}. Error: {str(e)}"
            except OSError:
                error_msg = f"Corrupted JSON file at {filepath}. Failed to create backup. Error: {str(e)}"
            
            raise JSONFileError(error_msg)
        except PermissionError:
            raise JSONFileError(f"Permission denied: Cannot read file {filepath}")
        except OSError as e:
            raise JSONFileError(f"Error reading file {filepath}: {str(e)}")
    
    def write_data(self, data: Dict, date_obj: Optional[date] = None) -> None:
        """
        Write complete data to a specific date's file. Creates a new file if it doesn't exist.
        
        Args:
            data (dict): Data to write to the file
            date_obj (date, optional): Date to write to. Defaults to current date.
            
        Raises:
            JSONFileError: If there's an error writing to the file
            TypeError: If the data cannot be serialized to JSON
        """
        filepath = self.storage_dir / self.get_filename(date_obj)
        
        # Ensure parent directory exists
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise JSONFileError(f"Permission denied: Cannot create directory {filepath.parent}")
        except OSError as e:
            raise JSONFileError(f"Error creating directory {filepath.parent}: {str(e)}")
        
        try:
            # Create a temporary file to ensure atomic writes
            temp_filepath = filepath.with_suffix('.tmp')
            with temp_filepath.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, cls=DateTimeEncoder)
            
            # Atomic replace operation
            temp_filepath.replace(filepath)
        except PermissionError:
            raise JSONFileError(f"Permission denied: Cannot write to file {filepath}")
        except TypeError as e:
            raise TypeError(f"JSON serialization error: {str(e)}")
        except OSError as e:
            raise JSONFileError(f"Error writing to file {filepath}: {str(e)}")
    
    def update_data(self, key: str, value: Any, date_obj: Optional[date] = None) -> None:
        """
        Update or add a specific key-value pair in the JSON file.
        
        Args:
            key (str): Key to update
            value (Any): Value to set
            date_obj (date, optional): Date of file to update. Defaults to current date.
            
        Raises:
            JSONFileError: If there's an error reading or writing the file
            TypeError: If the key is not a string or the value cannot be serialized
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        try:
            data = self.read_data(date_obj)
            data[key] = value
            self.write_data(data, date_obj)
        except (JSONFileError, TypeError) as e:
            raise e
    
    def append_to_list(self, key: str, value: Any, date_obj: Optional[date] = None) -> None:
        """
        Append a value to a list at the specified key. Creates list if it doesn't exist.
        
        Args:
            key (str): Key where list is stored
            value (Any): Value to append to the list
            date_obj (date, optional): Date of file to update. Defaults to current date.
            
        Raises:
            JSONFileError: If there's an error reading or writing the file
            TypeError: If the key is not a string or the value cannot be serialized
            ValueError: If the key exists but is not a list
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        try:
            data = self.read_data(date_obj)
            if key not in data:
                data[key] = []
            elif not isinstance(data[key], list):
                raise ValueError(f"Key '{key}' exists but is not a list")
                
            data[key].append(value)
            self.write_data(data, date_obj)
        except (JSONFileError, TypeError) as e:
            raise e
    
    def delete_key(self, key: str, date_obj: Optional[date] = None) -> bool:
        """
        Delete a key from the JSON file.
        
        Args:
            key (str): Key to delete
            date_obj (date, optional): Date of file to update. Defaults to current date.
            
        Returns:
            bool: True if key was deleted, False if key didn't exist
            
        Raises:
            JSONFileError: If there's an error reading or writing the file
            TypeError: If the key is not a string
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        try:
            data = self.read_data(date_obj)
            if key in data:
                del data[key]
                self.write_data(data, date_obj)
                return True
            return False
        except JSONFileError as e:
            raise e
    
    def get_all_dates(self) -> List[date]:
        """
        Get list of all dates that have JSON files.
        
        Returns:
            List[date]: List of dates with existing files
            
        Raises:
            JSONFileError: If there's an error accessing the storage directory
        """
        dates = []
        try:
            for file in self.storage_dir.glob("*.json"):
                try:
                    date_str = file.stem  # Get filename without extension
                    year, month, day = map(int, date_str.split("_"))
                    dates.append(date(year, month, day))
                except (ValueError, IndexError):
                    # Skip files that don't match our date format
                    continue
        except OSError as e:
            raise JSONFileError(f"Error accessing storage directory: {str(e)}")
            
        return sorted(dates)