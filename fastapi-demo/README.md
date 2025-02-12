# FastAPI Demo

This is a simple demo of FastAPI using Python 3.12. It demonstrates how to create a simple API with FastAPI.

## Features

- RESTful API
- CRUD operations

## Getting Started

### Requirements

- Python 3.12
- Poetry

### Development

1. Formatting

   ```bash
   poetry run black .  # Formats entire project
   ```

2. Linting

   ```bash
   poetry run ruff check .  # Base linting
   poetry run ruff check --fix .  # Auto-fix lint errors
   poetry run ruff check --watch .  # Watch mode

   ```

### Installation

1. Clone the repository

   ```bash
   git clone
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Run the development server:

   ```bash
   poetry run uvicorn fastapi_demo.main:app --reload
   ```

4. Open your browser and navigate to `http://localhost:8000/api/docs` to view the API documentation.
