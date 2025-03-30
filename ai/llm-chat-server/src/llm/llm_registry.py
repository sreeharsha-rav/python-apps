from typing import Dict, List
from src.llm.models.base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from models.openai_gpt4o_mini import OpenAIGPT4oMini
from models.azure_gpt4o_mini import AzureGPT4oMini
from models.google_gemini2_flash import GoogleGemini2Flash
from src.exceptions.llm import ModelNotFoundError

@singleton
class LLMRegistry:
    """Registry for managing LLM models"""
    
    _models: Dict[ModelID, BaseLLM] = {
        ModelID.AZURE_GPT4O_MINI: AzureGPT4oMini(),
        ModelID.GOOGLE_GEMINI2_FLASH: GoogleGemini2Flash(),
        ModelID.OPENAI_GPT4O_MINI: OpenAIGPT4oMini(),
    }

    def list_models(self) -> List[ModelInfo]:
        """List all available models with their information"""
        return [model.MODEL_INFO for model in self._models.values()]

    def get_model_info(self, model_id: str) -> ModelInfo:
        """Get model information for a specific model"""
        try:
            model_enum = ModelID(model_id)
            return self._models[model_enum].MODEL_INFO
        except (ValueError, KeyError):
            raise ModelNotFoundError(
                f"Invalid model_id: {model_id}. "
                f"Supported models: {[m.value for m in ModelID]}"
            )

    def get_model(self, model_id: str) -> BaseLLM:
        """
        Get the LLM instance for the specified model_id

        Args:
            model_id: The ID of the model to retrieve

        Returns:
            An instance of the specified LLM

        Raises:
            ModelNotFoundError: If the model_id is not found or invalid
        """
        try:
            model_enum = ModelID(model_id)
            return self._models[model_enum]
        except ValueError:
            raise ModelNotFoundError(
                f"Invalid model_id: {model_id}. "
                f"Supported models: {[m.value for m in ModelID]}"
            )