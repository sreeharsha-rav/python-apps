from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """
    Schema for creating a new item.

    Attributes:
        name (str): The name of the item (min length: 3 characters)
        price (float): The price of the item (must be greater than 0)
        description (Optional[str]): Optional description of the item
    """

    name: str = Field(
        ..., min_length=3, description="Name of the item", example="Coffee Mug"
    )
    price: float = Field(..., gt=0, description="Price of the item", example=9.99)
    description: str | None = Field(
        None,
        description="Optional description of the item",
        example="A ceramic coffee mug with company logo",
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Coffee Mug",
                "price": 9.99,
                "description": "A ceramic coffee mug with company logo",
            }
        }


class Item(ItemCreate):
    """
    Schema for a complete item, including its ID.

    Inherits all fields from ItemCreate and adds:
        id (UUID): Unique identifier for the item
    """

    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the item"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Coffee Mug",
                "price": 9.99,
                "description": "A ceramic coffee mug with company logo",
            }
        }
