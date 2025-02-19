import pytest
from datetime import datetime
from pathlib import Path
import shutil
from fleeting_thoughts.manager import ThoughtsManager

@pytest.fixture
def temp_storage(tmp_path):
    storage_dir = tmp_path / "test_thoughts"
    storage_dir.mkdir()
    yield storage_dir
    shutil.rmtree(storage_dir)

def test_add_thought(temp_storage):
    manager = ThoughtsManager(str(temp_storage))
    content = "Test thought"
    
    thought = manager.add_thought(content)
    
    assert thought.content == content
    assert isinstance(thought.timestamp, datetime)
    
    # Verify storage
    date = datetime.now().date().isoformat()
    daily_thoughts = manager.get_thoughts_for_date(date)
    assert daily_thoughts is not None
    assert len(daily_thoughts.thoughts) == 1
    assert daily_thoughts.thoughts[0].content == content

# Example usage
if __name__ == "__main__":
    manager = ThoughtsManager()
    
    # Add some thoughts
    manager.add_thought(
        "The sunset today reminded me of childhood memories at the beach. Need to call mom this weekend."
    )
    manager.add_thought(
        "Must remember to pick up groceries on the way home. Running low on coffee."
    )
    
    # Get today's thoughts
    today = datetime.now().date().isoformat()
    thoughts = manager.get_thoughts_for_date(today)
    if thoughts:
        print("Today's thoughts:")
        for thought in thoughts.thoughts:
            print(f"[{thought.timestamp}] {thought.content}")