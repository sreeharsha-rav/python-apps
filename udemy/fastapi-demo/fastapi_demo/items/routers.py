from fastapi import APIRouter, HTTPException, status

from fastapi_demo.items.models import Item, ItemCreate
from fastapi_demo.items.service import item_service

item_router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with ID {item_id} not found"}
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {"example": {"detail": "Internal server error"}}
            },
        },
    },
)


@item_router.get(
    "",
    response_model=list[Item],
    summary="Get all items",
    description="Retrieve a list of all items in the store.",
    responses={
        status.HTTP_200_OK: {
            "description": "List of items retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Coffee Mug",
                            "price": 9.99,
                            "description": "A ceramic coffee mug with company logo",
                        }
                    ]
                }
            },
        }
    },
)
async def get_items():
    """Get all items."""
    return await item_service.get_all()


@item_router.get(
    "/{item_id}",
    response_model=Item,
    summary="Get item by ID",
    description="Retrieve a specific item by its ID.",
    responses={
        status.HTTP_200_OK: {
            "description": "Item retrieved successfully",
            "model": Item,
        }
    },
)
async def get_item(item_id: str):
    """Get a specific item by ID."""
    item = await item_service.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return item


@item_router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create new item",
    description="Create a new item in the store.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Item created successfully",
            "model": Item,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "price"],
                                "msg": "ensure this value is greater than 0",
                                "type": "value_error.number.not_gt",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def create_item(item: ItemCreate):
    """Create a new item."""
    return await item_service.create(item)


@item_router.put(
    "/{item_id}",
    response_model=Item,
    summary="Update item",
    description="Update an existing item by its ID.",
    responses={
        status.HTTP_200_OK: {"description": "Item updated successfully", "model": Item}
    },
)
async def update_item(item_id: str, item: ItemCreate):
    """Update an existing item."""
    updated_item = await item_service.update(item_id, item)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return updated_item


@item_router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item",
    description="Delete an item by its ID.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Item deleted successfully"}
    },
)
async def delete_item(item_id: str):
    """Delete an item."""
    success = await item_service.delete(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return None
