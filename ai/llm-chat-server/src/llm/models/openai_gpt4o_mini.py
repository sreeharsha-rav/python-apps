from base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.exceptions.llm  import ConfigurationError, ClientInitializationError, GenerateCompletionError
from typing import ClassVar
import os
import openai

@singleton
class OpenAIGPT4oMini(BaseLLM):
    """OpenAI GPT-4o-mini LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.OPENAI_GPT4O_MINI,
        name="GPT-4o-mini",
        description="A smaller version of the GPT-4o model, optimized for faster inference and lower resource usage hosted on OpenAI",
        provider="OpenAI",
        context_length=128000,
        max_output_tokens=16384,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            
            # Validate required environment variables
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL")
            
            if not self.api_key:
                raise ConfigurationError("OPENAI_API_KEY environment variable is not set")
            if not self.model:
                raise ConfigurationError("OPENAI_MODEL environment variable is not set")
            
            try:
                self.client = openai.Client(api_key=self.api_key)
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize OpenAI client: {str(e)}")
            
            self._initialized = True

    async def get_completion(self, message: str) -> str:
        """Get completion from OpenAI GPT-4o-mini model"""
        if not message.strip():
            raise ConfigurationError("Message cannot be empty")
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
