from abc import ABC, abstractmethod
from Utils.Models.OpenAI.user_message_model import UserMessageModel

from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel


class OpenAiServiceBase(ABC):

    @abstractmethod
    def message(self, message: UserMessageModel) -> OpenAiResponseModel:
        pass
