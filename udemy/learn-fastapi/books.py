from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    book_id: int
    title: str
    author: str
    category: str
    rating: float
    published_year: int

    def __init__(self, book_id: int, title: str, author: str, category: str, rating: float, published_year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    book_id: Optional[int] = Field(gt=0, description="Book id")
    title: str = Field(min_length=3, max_length=100, description="Book title")
    author: str = Field(min_length=3, max_length=100, description="Book author")
    category: str = Field(min_length=3, max_length=100, description="Book category")
    rating: float = Field(ge=1, le=5, description="Book rating")
    published_year: int = Field(ge=1900, le=2025, description="Book published year")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "book_id": 1,
                    "title": "The Great Gatsby",
                    "author": "F. Scott Fitzgerald",
                    "category": "Fiction",
                    "rating": 4.5,
                    "published_year": 1925,
                }
            ]
        }
    }

BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 4.5, 1925),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", 4.0, 1960),
    Book(3, "1984", "George Orwell", "Fiction", 4.5, 1949),
    Book(4, "The Catcher in the Rye", "J.D. Salinger", "Fiction", 3.5, 1951),
    Book(5, "The Hobbit", "J.R.R. Tolkien", "Fantasy", 4.5, 1937),
]

@app.get("/books", status_code=200)
async def read_all_books():
    """Get all books"""
    return BOOKS

@app.post("/books", status_code=201)
async def create_book(book_request: BookRequest):
    """Create a book"""
    new_book = Book(**book_request.model_dump())
    new_book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    BOOKS.append(new_book)
    return {"message": "Book created", "book_id": new_book.book_id}

@app.get("/books/{book_id}", status_code=200)
async def read_book(book_id: int = Path(gt=0)):
    """Get a book by id"""
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.get("/books/", status_code=200)
async def read_book_by_query(
        title: Optional[str] = Query(None, min_length=3, max_length=100, description="filter by title"),
        author: Optional[str] = Query(None, min_length=3, max_length=100, description="filter by author"),
        category: Optional[str] = Query(None, min_length=3, max_length=100, description="filter by category"),
        rating: Optional[float] = Query(None, ge=1, le=5, description="filter by rating"),
        published_year: Optional[int] = Query(None, ge=1900, le=2025, description="filter by published year")
):
    """Get a book by query parameters"""
    books = []
    for book in BOOKS:
        if (title is None or book.title == title) and \
           (author is None or book.author == author) and \
           (category is None or book.category == category) and \
           (rating is None or book.rating == rating) and \
           (published_year is None or book.published_year == published_year):
            books.append(book)
    if not books:
        raise HTTPException(status_code=404, detail="No books found matching the criteria")
    return books

@app.put("/books/{book_id}", status_code=200)
async def update_book(
        book_id: int = Path(gt=0),
        book_request: BookRequest = None
):
    """Update a book"""
    if book_request is None:
        raise HTTPException(status_code=400, detail="Book request data is required")

    for idx, book in enumerate(BOOKS):
        if book.book_id == book_id:
            BOOKS[idx] = Book(**book_request.model_dump())
            BOOKS[idx].book_id = book_id         # preserve the id
            return {"message": "Book updated", "book_id": book_id}
    
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int = Path(gt=0)):
    """Delete a book"""
    for idx, book in enumerate(BOOKS):
        if book.book_id == book_id:
            BOOKS.pop(idx)
            return None  # 204 No Content should return no body
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
