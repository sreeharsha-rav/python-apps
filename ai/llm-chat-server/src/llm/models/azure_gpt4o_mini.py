from base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.exceptions.llm import ConfigurationError, ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from openai.lib.azure import AzureOpenAI
import os

@singleton
class AzureGPT4oMini(BaseLLM):
    """Azure GPT-4o-mini LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.AZURE_GPT4O_MINI,
        name="GPT-4o-mini",
        description="A smaller version of the GPT-4o model, optimized for faster inference and lower resource usage hosted on Azure",
        provider="Azure",
        context_length=128000,
        max_output_tokens=16384,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            
            # Validate required environment variables
            self.api_key = os.getenv("AZURE_GPT4O_MINI_API_KEY")
            self.endpoint = os.getenv("AZURE_GPT4O_MINI_API_ENDPOINT")
            self.api_version = os.getenv("AZURE_GPT4O_MINI_API_VERSION")
            self.deployment_id = os.getenv("AZURE_GPT4O_MINI_DEPLOYMENT_ID")

            if not self.api_key:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_KEY environment variable is not set")
            if not self.endpoint:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_ENDPOINT environment variable is not set")
            if not self.api_version:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_VERSION environment variable is not set")
            if not self.deployment_id:
                raise ConfigurationError("AZURE_GPT4O_MINI_DEPLOYMENT_ID environment variable is not set")

            try:
                self.client = AzureOpenAI(
                    azure_endpoint=self.endpoint,
                    api_key=self.api_key,
                    api_version=self.api_version,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Azure OpenAI client: {str(e)}")
                
            self._initialized = True

    async def get_completion(self, message: str) -> str:
        """Get completion from Azure GPT-4o-mini model"""
        if not message.strip():
            raise ConfigurationError("Message cannot be empty")
            
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_id,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
