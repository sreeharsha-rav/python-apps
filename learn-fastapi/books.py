from fastapi import FastAPI, Body
from middleware import LogRequestsMiddleware, configure_logging

# Configure logging before app startup
configure_logging()

app = FastAPI()

# Add logging middleware
app.add_middleware(LogRequestsMiddleware)


BOOKS = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'Classic'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'category': 'Dystopian'},
    {'id': 3, 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
    {'id': 4, 'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'category': 'Classic'},
    {'id': 5, 'title': 'Brave New World', 'author': 'Aldous Huxley', 'category': 'Dystopian'},
]

@app.get("/books")
async def read_all_books(category: str = None):
    """
    Get all books, optionally filtered by category (Query Parameter).
    """
    if category:
        books_to_return = []
        for book in BOOKS:
            if book.get('category').casefold() == category.casefold():
                books_to_return.append(book)
        return books_to_return
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    """
    Get a specific book by ID (Path Parameter).
    """
    for book in BOOKS:
        if book.get('id') == book_id:
            return book
    return {"message": "Book not found"}

@app.post("/books")
async def create_book(new_book=Body()):
    """
    Create a new book (Request Body).
    """
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book=Body()):
    """
    Update an existing book by ID (Path Parameter + Request Body).
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get('id') == book_id:
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"message": "Book not found"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """
    Delete a book by ID (Path Parameter).
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get('id') == book_id:
            deleted_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": deleted_book}
    return {"message": "Book not found"}
