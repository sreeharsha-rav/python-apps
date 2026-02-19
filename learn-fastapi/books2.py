from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from middleware import LogRequestsMiddleware, configure_logging

# Configure logging
configure_logging()

app = FastAPI(
    title="Books API v2",
    description="A simple API to manage books with validation and error handling.",
    version="2.0.0"
)

# Add middleware
app.add_middleware(LogRequestsMiddleware)


class BookRequest(BaseModel):
    """
    Pydantic model for Book request body validation.
    """
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6, description="Rating between 1-5")
    published_year: int = Field(gt=1900, lt=2100, description="Year between 1900 and 2100")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A New Design",
                "author": "Sreeharsha",
                "description": "A book about API design",
                "rating": 5,
                "published_year": 2024
            }
        }
    }


class Book:
    """
    Simple class to represent a Book in our internal database (list).
    """
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_year: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


# In-memory database
BOOKS = [
    Book(1, "Computer Science Pro", "Sreeharsha", "A nice book", 5, 2020),
    Book(2, "FastAPI for APIs", "Sreeharsha", "Great book", 5, 2023),
    Book(3, "Mastering Python", "Sreeharsha", "Awesome book", 5, 2024),
    Book(4, "HP1", "J.K. Rowling", "Harry Potter 1", 5, 1997),
    Book(5, "HP2", "J.K. Rowling", "Harry Potter 2", 5, 1998),
]


@app.get("/books", status_code=status.HTTP_200_OK, tags=["books"])
async def read_all_books():
    """
    Retrieve all books.
    """
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK, tags=["books"])
async def read_book(book_id: int = Path(gt=0)):
    """
    Retrieve a specific book by ID.
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK, tags=["books"])
async def read_books_by_publish_year(published_year: int = Query(gt=1900, lt=2100)):
    """
    Filter books by published year using Query parameters.
    """
    books_to_return = [book for book in BOOKS if book.published_year == published_year]
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED, tags=["books"])
async def create_book(book_request: BookRequest):
    """
    Create a new book using a Pydantic Request Object.
    Auto-increments ID if not provided.
    """
    new_book_dict = book_request.model_dump()
    
    # Simple ID generation strategy
    new_id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
    # Use provided ID if it's set and valid (optional logic, usually we ignore/overwrite ID on create)
    # Here we strictly generate a new ID to ensure uniqueness in our list
    new_book = Book(
        id=new_id,
        title=new_book_dict['title'],
        author=new_book_dict['author'],
        description=new_book_dict['description'],
        rating=new_book_dict['rating'],
        published_year=new_book_dict['published_year']
    )
    
    BOOKS.append(new_book)
    return new_book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
async def update_book(book: BookRequest):
    """
    Update a book. Requires ID in the request body.
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump()) # Replaces the object
            book_changed = True
            break
            
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
async def delete_book(book_id: int = Path(gt=0)):
    """
    Delete a book by ID.
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
            
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
