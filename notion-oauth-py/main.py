from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware
from middleware import LogRequestsMiddleware, configure_logging
from notion_oauth.router import router as oauth_router

# Configure logging
configure_logging()

app = FastAPI(
    title="Notion OAuth Demo",
    description="A simple demo of Notion OAuth with MCP",
    version="1.0.0"
)

# Add session middleware (required for OAuth flow)
# In production, use a secure random key and store it in environment variables
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-change-in-production",  # TODO: Move to .env
    max_age=3600  # Session expires after 1 hour
)

# Add logging middleware
app.add_middleware(LogRequestsMiddleware)

# Include OAuth router
app.include_router(oauth_router)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

