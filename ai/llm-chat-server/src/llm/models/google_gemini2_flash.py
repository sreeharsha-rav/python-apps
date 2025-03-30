from base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.exceptions.llm  import ConfigurationError, ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from google.genai import Client
import os

@singleton
class GoogleGemini2Flash(BaseLLM):
    """Google Gemini 2.0 Flash LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.GOOGLE_GEMINI2_FLASH,
        name="Gemini 2.0 Flash",
        description="A flash-optimized version of the Gemini 2.0 model, designed for faster inference and lower resource usage hosted on Google",
        provider="Google",
        context_length=1048576,
        max_output_tokens=8192,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            
            # Validate required environment variables
            self.model = os.getenv("GOOGLE_GEMINI2_FLASH_MODEL")
            
            if not self.model:
                raise ConfigurationError("GOOGLE_GEMINI2_FLASH_MODEL environment variable is not set")
            
            try:
                self.client = Client(
                    vertexai=os.getenv("GOOGLE_GENAI_USE_VERTEXAI"),
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Google Gemini client: {str(e)}")
                
            self._initialized = True

    async def get_completion(self, message: str) -> str:
        """Get completion from Google Gemini 2.0 Flash model"""
        if not message.strip():
            raise ConfigurationError("Message cannot be empty")
            
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=message,
            )
            return response.text
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
