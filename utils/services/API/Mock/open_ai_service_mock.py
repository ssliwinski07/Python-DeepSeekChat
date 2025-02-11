from typing import List
import random

from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel
from Utils.Models.OpenAI.openai_choice_model import OpenAiChoiceModel
from Utils.Models.OpenAI.openai_message_model import OpenAiMessageModel


class OpenAiServiceMock(OpenAiServiceBase):

    def open_client(self):
        """
        Mock implementation of open_client.
        This method is intentionally empty as no real API client needs to be initialized for the mock service.
        """
        pass

    def message(self, messages: List[dict]) -> OpenAiResponseModel:

        try:
            responses = [
                "Gosia is beautiful!",
                "I'm a mock AI assistant.",
                "Cats are cool!",
                "Mock mode active. Switch to production mode to use actual AI capabilities.",
            ]

            choices = [
                OpenAiChoiceModel(
                    message=OpenAiMessageModel(content=random.choice(responses))
                )
            ]

            result: OpenAiResponseModel = OpenAiResponseModel(choices=choices)

            return result
        except Exception as e:
            raise ValueError(f"Error in mock service: {str(e)}")
