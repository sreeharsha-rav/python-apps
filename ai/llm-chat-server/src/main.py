from fastapi import FastAPI
from src.routers.v1 import chat, models
from src.config.settings import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Outputs to console
    ]
)

# Set debug level for our chat module
logging.getLogger('src.routers.v1.chat').setLevel(logging.DEBUG)

app = FastAPI(
    title="LLM Chat Server",
    description="A server for chat with LLMs",
    version="0.1.0",
)

@app.get("/health")
def get_status():
    """Health check endpoint"""
    return {
        "status": "ok",
        "environment": {
            "openai_gpt4o_mini_configured": bool(settings.OPENAI_API_KEY),
            "azure_gpt4o_mini_configured": bool(settings.AZURE_GPT4O_MINI_API_KEY),
            "google_gemini2_flash_configured": bool(settings.GOOGLE_GEMINI2_FLASH_MODEL)
        }
    }

# Register api routes
app.include_router(chat.router, prefix="/api")
app.include_router(models.router, prefix="/api")
