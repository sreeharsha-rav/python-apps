import json
import os
import shutil
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from main.storage.json_file_manager import JSONFileManager, JSONFileError, DateTimeEncoder


class TestJSONFileManager:
    """Test suite for JSONFileManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after test
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def manager(self, temp_dir):
        """Create a JSONFileManager instance for testing."""
        return JSONFileManager(temp_dir)

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return {
            "key1": "value1",
            "key2": 123,
            "key3": ["item1", "item2"],
            "key4": {"nested": "value"}
        }

    @pytest.fixture
    def today(self):
        """Get today's date."""
        return datetime.now().date()

    def test_init(self, temp_dir):
        """Test initialization creates directory if it doesn't exist."""
        # Directory doesn't exist yet
        new_dir = os.path.join(temp_dir, "new_dir")
        assert not os.path.exists(new_dir)

        # Initialize manager
        manager = JSONFileManager(new_dir)
        
        # Directory should be created
        assert os.path.exists(new_dir)
        assert isinstance(manager.get_storage_dir(), Path)

    def test_init_permission_error(self, temp_dir):
        """Test initialization handles permission error."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Permission denied")
            
            with pytest.raises(JSONFileError) as excinfo:
                JSONFileManager(temp_dir)
            
            assert "Permission denied" in str(excinfo.value)

    def test_init_os_error(self, temp_dir):
        """Test initialization handles OS error."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = OSError("Some OS error")
            
            with pytest.raises(JSONFileError) as excinfo:
                JSONFileManager(temp_dir)
            
            assert "Failed to create storage directory" in str(excinfo.value)

    def test_get_filename(self, manager):
        """Test get_filename method."""
        test_date = date(2023, 5, 15)
        filename = manager.get_filename(test_date)
        assert filename == "2023_05_15.json"
        
        # Test default to current date
        today = datetime.now().date()
        expected = f"{today.strftime('%Y_%m_%d')}.json"
        assert manager.get_filename() == expected

    def test_file_exists(self, manager, temp_dir):
        """Test file_exists method."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # File doesn't exist yet
        assert not manager.file_exists(test_date)
        
        # Create file
        with open(filepath, 'w') as f:
            f.write("{}")
        
        # File should exist now
        assert manager.file_exists(test_date)

    def test_read_data_file_not_found(self, manager):
        """Test read_data method when file doesn't exist."""
        test_date = date(2023, 5, 15)
        # File doesn't exist, should return empty dict
        assert manager.read_data(test_date) == {}

    def test_read_data_success(self, manager, temp_dir, sample_data):
        """Test read_data method with existing file."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create file with sample data
        with open(filepath, 'w') as f:
            json.dump(sample_data, f)
        
        # Read data
        data = manager.read_data(test_date)
        assert data == sample_data

    def test_read_data_json_decode_error(self, manager, temp_dir):
        """Test read_data method with corrupted JSON."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create corrupted JSON file
        with open(filepath, 'w') as f:
            f.write("{invalid json")
        
        # Read data should raise JSONFileError
        with pytest.raises(JSONFileError) as excinfo:
            manager.read_data(test_date)
            
        assert "Corrupted JSON file" in str(excinfo.value)
        
        # Check if backup file was created
        backup_path = filepath + ".bak"
        assert os.path.exists(backup_path)

    def test_read_data_permission_error(self, manager):
        """Test read_data method with permission error."""
        test_date = date(2023, 5, 15)
        
        # Patch Path.open instead of builtins.open
        with patch('pathlib.Path.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(JSONFileError) as excinfo:
                manager.read_data(test_date)
                
            assert "Permission denied" in str(excinfo.value)

    def test_read_data_os_error(self, manager):
        """Test read_data method with OS error."""
        test_date = date(2023, 5, 15)
        
        # Patch Path.open instead of builtins.open
        with patch('pathlib.Path.open', side_effect=OSError("Some OS error")):
            with pytest.raises(JSONFileError) as excinfo:
                manager.read_data(test_date)
                
            assert "Error reading file" in str(excinfo.value)

    def test_write_data(self, manager, temp_dir, sample_data):
        """Test write_data method."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Write data
        manager.write_data(sample_data, test_date)
        
        # Check file exists
        assert os.path.exists(filepath)
        
        # Check file contents
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data == sample_data

    def test_write_data_with_datetime(self, manager, temp_dir):
        """Test write_data method with datetime objects."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Data with datetime objects
        data = {
            "date": date(2023, 5, 15),
            "datetime": datetime(2023, 5, 15, 12, 30, 0)
        }
        
        # Write data
        manager.write_data(data, test_date)
        
        # Check file exists
        assert os.path.exists(filepath)
        
        # Check file contents are serialized correctly
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
            assert loaded_data["date"] == "2023-05-15"
            assert loaded_data["datetime"] == "2023-05-15T12:30:00"

    def test_write_data_permission_error_directory(self, manager):
        """Test write_data method with directory permission error."""
        test_date = date(2023, 5, 15)
        
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
            with pytest.raises(JSONFileError) as excinfo:
                manager.write_data({}, test_date)
                
            assert "Permission denied" in str(excinfo.value)
            assert "Cannot create directory" in str(excinfo.value)

    def test_write_data_permission_error_file(self, manager):
        """Test write_data method with file permission error."""
        test_date = date(2023, 5, 15)
        
        with patch('pathlib.Path.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(JSONFileError) as excinfo:
                manager.write_data({}, test_date)
                
            assert "Permission denied" in str(excinfo.value)
            assert "Cannot write to file" in str(excinfo.value)

    def test_write_data_type_error(self, manager):
        """Test write_data method with non-serializable data."""
        test_date = date(2023, 5, 15)
        
        # Create data with non-serializable object
        class NonSerializable:
            pass
        
        data = {"key": NonSerializable()}
        
        with pytest.raises(TypeError) as excinfo:
            manager.write_data(data, test_date)
            
        assert "JSON serialization error" in str(excinfo.value)

    def test_update_data(self, manager, temp_dir, sample_data):
        """Test update_data method."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create initial file
        with open(filepath, 'w') as f:
            json.dump(sample_data, f)
        
        # Update data
        manager.update_data("new_key", "new_value", test_date)
        
        # Check file exists
        assert os.path.exists(filepath)
        
        # Check file contents
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert "new_key" in data
            assert data["new_key"] == "new_value"
            # Original data should still be there
            assert data["key1"] == "value1"

    def test_update_data_key_type_error(self, manager):
        """Test update_data method with invalid key type."""
        with pytest.raises(TypeError) as excinfo:
            manager.update_data(123, "value")
            
        assert "Key must be a string" in str(excinfo.value)

    def test_append_to_list(self, manager, temp_dir):
        """Test append_to_list method."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create initial file
        initial_data = {"existing_list": ["item1"]}
        with open(filepath, 'w') as f:
            json.dump(initial_data, f)
        
        # Append to existing list
        manager.append_to_list("existing_list", "item2", test_date)
        
        # Check file contents
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data["existing_list"] == ["item1", "item2"]
        
        # Append to new list
        manager.append_to_list("new_list", "first_item", test_date)
        
        # Check file contents again
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data["new_list"] == ["first_item"]

    def test_append_to_list_key_not_list(self, manager, temp_dir):
        """Test append_to_list method with non-list key."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create initial file
        initial_data = {"not_a_list": "string_value"}
        with open(filepath, 'w') as f:
            json.dump(initial_data, f)
        
        # Append to non-list key should raise ValueError
        with pytest.raises(ValueError) as excinfo:
            manager.append_to_list("not_a_list", "item", test_date)
            
        assert "is not a list" in str(excinfo.value)

    def test_delete_key(self, manager, temp_dir, sample_data):
        """Test delete_key method."""
        test_date = date(2023, 5, 15)
        filename = test_date.strftime('%Y_%m_%d') + ".json"
        filepath = os.path.join(temp_dir, filename)
        
        # Create initial file
        with open(filepath, 'w') as f:
            json.dump(sample_data, f)
        
        # Delete existing key
        result = manager.delete_key("key1", test_date)
        
        # Check result
        assert result is True
        
        # Check file contents
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert "key1" not in data
            assert "key2" in data
        
        # Delete non-existing key
        result = manager.delete_key("non_existent_key", test_date)
        
        # Check result
        assert result is False

    def test_delete_key_type_error(self, manager):
        """Test delete_key method with invalid key type."""
        with pytest.raises(TypeError) as excinfo:
            manager.delete_key(123)
            
        assert "Key must be a string" in str(excinfo.value)

    def test_get_all_dates(self, manager, temp_dir):
        """Test get_all_dates method."""
        # Create several date files
        dates = [
            date(2023, 5, 15),
            date(2023, 5, 16),
            date(2023, 5, 17)
        ]
        
        for d in dates:
            filename = d.strftime('%Y_%m_%d') + ".json"
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write("{}")
        
        # Also create a file with invalid date format
        with open(os.path.join(temp_dir, "invalid_format.json"), 'w') as f:
            f.write("{}")
        
        # Get all dates
        result = manager.get_all_dates()
        
        # Check result
        assert len(result) == len(dates)
        assert result == sorted(dates)
        assert date(2023, 5, 15) in result
        assert date(2023, 5, 16) in result
        assert date(2023, 5, 17) in result

    def test_get_all_dates_os_error(self, manager):
        """Test get_all_dates method with OS error."""
        with patch('pathlib.Path.glob', side_effect=OSError("Access denied")):
            with pytest.raises(JSONFileError) as excinfo:
                manager.get_all_dates()
                
            assert "Error accessing storage directory" in str(excinfo.value)

    def test_date_encoder(self):
        """Test the DateTimeEncoder class."""
        encoder = DateTimeEncoder()
        test_date = date(2023, 5, 15)
        test_datetime = datetime(2023, 5, 15, 12, 30, 0)
        
        # Test date serialization
        assert encoder.default(test_date) == "2023-05-15"
        
        # Test datetime serialization
        assert encoder.default(test_datetime) == "2023-05-15T12:30:00"
        
        # Test error for unsupported types
        with pytest.raises(TypeError):
            encoder.default(object())