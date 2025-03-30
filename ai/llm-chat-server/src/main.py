from fastapi import FastAPI
from dotenv import load_dotenv
from src.routers.v1 import chat, conversation

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="LLM Chat Server",
    description="A server for chat with LLMs",
    version="0.1.0",
)

@app.get("/health")
def get_status():
    """Health check endpoint"""
    return {"status": "ok"}

# Register api routes
app.include_router(chat.router, prefix="/api")
app.include_router(conversation.router, prefix="/api")
