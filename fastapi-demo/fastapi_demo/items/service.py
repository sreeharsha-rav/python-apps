from fastapi_demo.items.models import Item, ItemCreate


class ItemService:
    """Service class for managing items in memory."""

    def __init__(self):
        """Initialize an empty list of items."""
        self.items: list[Item] = []

    async def get_all(self) -> list[Item]:
        """
        Retrieve all items.

        Returns:
            list[Item]: List of all items in the store
        """
        print("Fetching all items")
        return self.items

    async def get(self, item_id: str) -> Item | None:
        """
        Retrieve a specific item by ID.

        Args:
            item_id (str): The ID of the item to retrieve

        Returns:
            Optional[Item]: The item if found, None otherwise
        """
        print(f"Fetching item: {item_id}")
        for item in self.items:
            if str(item.id) == item_id:
                return item
        return None

    async def create(self, item: ItemCreate) -> Item:
        """
        Create a new item.

        Args:
            item (ItemCreate): The item data to create

        Returns:
            Item: The created item with generated ID
        """
        new_item = Item(**item.dict())
        self.items.append(new_item)
        print(f"Created item: {new_item.id}")
        return new_item

    async def update(self, item_id: str, item: ItemCreate) -> Item | None:
        """
        Update an existing item.

        Args:
            item_id (str): The ID of the item to update
            item (ItemCreate): The new item data

        Returns:
            Optional[Item]: The updated item if found, None otherwise
        """
        print(f"Updating item: {item_id}")
        for i, existing_item in enumerate(self.items):
            if str(existing_item.id) == item_id:
                updated_item = Item(**item.dict(), id=existing_item.id)
                self.items[i] = updated_item
                return updated_item
        return None

    async def delete(self, item_id: str) -> bool:
        """
        Delete an item.

        Args:
            item_id (str): The ID of the item to delete

        Returns:
            bool: True if the item was deleted, False otherwise
        """
        print(f"Deleting item: {item_id}")
        original_length = len(self.items)
        self.items = [item for item in self.items if str(item.id) != item_id]
        return len(self.items) < original_length


item_service = ItemService()
