from datetime import date
from json_storage.service import JSONFileManager

def main():
    # Initialize the JSON file manager
    manager = JSONFileManager("./test_data")
    print("Initialized JSONFileManager with test_data directory")

    # Test writing and reading data
    test_data = {
        "user": "Jane",
        "settings": {
            "theme": "light",
            "notifications": True
        },
        "scores": [85, 90, 78]
    }

    # get storage directory
    print("\n1. Getting storage directory...")
    print(f"Storage directory: {manager.get_storage_dir()}")

    # get filename
    print("\n2. Getting filename for today...")
    print(f"Today's filename: {manager.get_filename()}")

    # check file existence
    print("\n3. Checking file existence for today...")
    print(f"Today's file exists? {manager.file_exists()}")
    
    # # Write initial data
    # print("\n4. Writing initial test data for today...")
    # manager.write_data(test_data)
    
    # # Read and verify data
    # print("\n5. Reading back the data for today...")
    # retrieved_data = manager.read_data()
    # print(f"Retrieved data: {retrieved_data}")

    # Test updating specific key-value
    print("\n6. Updating a specific key...")
    manager.update_data("user", "John Doe")
    print("Updated data:", manager.read_data())

    # Test appending to a list
    print("\n4. Appending to a list...")
    manager.append_to_list("scores", 95)
    print("Data after append:", manager.read_data())

    # # Test data for a specific date
    # specific_date = date(2025, 2, 20)
    # print(f"\n5. Writing data for specific date ({specific_date})...")
    # manager.write_data({"meeting": "Team Sync"}, specific_date)
    
    # # Check file existence
    # print("\n6. Checking file existence...")
    # print(f"Does today's file exist? {manager.file_exists()}")
    # print(f"Does specific date file exist? {manager.file_exists(specific_date)}")

    # Delete a key
    print("\n7. Deleting a key...")
    deleted = manager.delete_key("name")
    print(f"Key deleted: {deleted}")
    print("Data after deletion:", manager.read_data())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")