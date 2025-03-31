# LLM Chat Server

A FastAPI-based server that provides a unified interface for interacting with various Large Language Models (LLMs) including OpenAI's GPT-4o-mini, Azure's GPT-4o-mini, and Google's Gemini 2.0 Flash.

## Prerequisites

- Python 3.12 or higher
- `uv` package manager (`pip install uv`)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-chat-server
```

2. Create and activate a virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Create environment variables file:
```bash
cp .env.example .env
```

5. Configure your `.env` file with appropriate API keys and settings:
- OpenAI credentials
- Azure credentials
- Google Cloud credentials

## Running the Server

### Local Development

Start the development server:
```bash
uv run uvicorn src.main:app --reload
```

The server will be available at `http://localhost:8000`

### Docker

#### Prerequisites
- Docker installed on your system
- Docker Compose (optional, for development)

#### Building and Running with Docker

1. Build the Docker image:
```bash
docker build -t llm-chat-server .
```

2. Run the container:
```bash
docker run -d \
    -p 8000:8000 \
    --name llm-chat-server \
    --env-file .env \
    llm-chat-server
```

#### Docker Commands

- Stop the container:
```bash
docker stop llm-chat-server
```

- Remove the container:
```bash
docker rm llm-chat-server
```

- View logs:
```bash
docker logs -f llm-chat-server
```

- Shell into container:
```bash
docker exec -it llm-chat-server /bin/bash
```

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Health Check

You can verify the server's status and configuration by accessing:
```bash
curl http://localhost:8000/health
```

This will return the status of configured LLM providers.

## Project Structure

```
llm-chat-server/
├── src/                        # Source code directory
│   ├── config/                 # Configuration management
│   │   ├── settings.py        # Environment and app settings
│   ├── exceptions/            # Custom exceptions
│   │   ├── chat.py           # Chat-related exceptions
│   │   ├── llm.py            # LLM-related exceptions
│   ├── llm/                   # LLM integration layer
│   │   ├── models/           # LLM model implementations
│   │   │   ├── base_llm.py   # Base LLM abstract class
│   │   │   ├── azure_gpt4o_mini.py    # Azure implementation
│   │   │   ├── google_gemini2_flash.py # Google implementation
│   │   │   └── openai_gpt4o_mini.py    # OpenAI implementation
│   │   └── llm_registry.py    # LLM model registry
│   ├── repositories/          # Data access layer
│   │   └── chat.py           # Chat storage operations
│   ├── routers/              # API route handlers
│   │   └── v1/              
│   │       ├── chat.py       # Chat endpoints
│   │       └── models.py     # Model info endpoints
│   ├── schemas/              # Pydantic models
│   │   ├── chat.py          # Chat-related schemas
│   │   └── llm.py           # LLM-related schemas
│   ├── services/            # Business logic layer
│   │   └── chat.py         # Chat service implementation
│   └── main.py             # Application entry point
├── .env.example            # Example environment variables
├── pyproject.toml         # Project metadata and dependencies
├── README.md             # Project documentation
└── uv.lock              # Dependency lock file
```

## Component Overview

### Core Components

- **main.py**: Application entry point, FastAPI app configuration, and route registration
- **settings.py**: Environment variable management using Pydantic
- **llm_registry.py**: Central registry for managing different LLM implementations

### LLM Integration

The `llm/models/` directory contains implementations for different LLM providers:
- `base_llm.py`: Abstract base class defining the LLM interface
- `azure_gpt4o_mini.py`: Azure's GPT-4o-mini implementation
- `google_gemini2_flash.py`: Google's Gemini 2.0 Flash implementation
- `openai_gpt4o_mini.py`: OpenAI's GPT-4o-mini implementation

### API Layer

- `routers/v1/chat.py`: Chat-related endpoints (create, list, get, delete)
- `routers/v1/models.py`: Model information endpoints
- `schemas/`: Request/response models using Pydantic

### Business Logic

- `services/chat.py`: Chat service handling message processing and LLM interactions
- `repositories/chat.py`: Chat storage operations (currently in-memory)

### Error Handling

- `exceptions/`: Custom exception classes for better error handling
  - `chat.py`: Chat-related exceptions
  - `llm.py`: LLM-related exceptions