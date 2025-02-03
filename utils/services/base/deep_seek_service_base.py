from abc import ABC, abstractmethod
from typing import List

from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel


class DeepSeekServiceBase(ABC):
    @abstractmethod
    def send_msg(self, messages: List[dict]) -> DeepSeekResponseModel:
        pass
