# FastAPI Learning

This repository is for learning FastAPI.

## Requirements

- Python 3.11+
- uv

## Setup and Run

```bash
# install dependencies
uv sync

# activate virtual environment

## windows
.venv\Scripts\activate

## linux/mac
source .venv/bin/activate

## run
uvicorn main:app --reload
```

## Testing

```bash
curl http://localhost:8000/docs
```
