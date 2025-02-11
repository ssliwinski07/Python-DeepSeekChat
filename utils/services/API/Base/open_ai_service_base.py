from abc import ABC, abstractmethod
from typing import List

from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel


class OpenAiServiceBase(ABC):
    """Base class for OpenAI service implementations."""

    @abstractmethod
    def open_client(self):
        pass

    @abstractmethod
    def message(self, messages: List[dict]) -> OpenAiResponseModel:
        """Send a message to OpenAI API and get a response."""
        pass
