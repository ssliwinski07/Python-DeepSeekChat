from abc import ABC, abstractmethod
from typing import List

from Utils.Models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel


class OpenAiServiceBase(ABC):

    @abstractmethod
    def open_client(self):
        pass

    @abstractmethod
    def message(self, messages: List[dict]) -> DeepSeekResponseModel:
        pass
