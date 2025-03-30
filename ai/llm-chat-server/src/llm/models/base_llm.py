from abc import ABC, abstractmethod
from typing import ClassVar
from src.schemas.llm import ModelInfo

class BaseLLM(ABC):
    """Base class for LLM implementations"""

    MODEL_INFO: ClassVar[ModelInfo]         # Static class variable for model information

    def __init__(self) -> None:
        """Initialize the LLM"""
        pass

    @abstractmethod
    async def get_completion(self, message: str) -> str:
        """
        Get completion from LLM
        
        Args:
            message: The input message to process
            
        Returns:
            The model's response
        """
        pass