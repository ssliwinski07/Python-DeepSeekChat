from typing import List
import random

from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel
from Utils.Models.OpenAI.openai_choice_model import OpenAiChoiceModel
from Utils.Models.OpenAI.openai_message_model import OpenAiMessageModel


class OpenAiServiceMock(OpenAiServiceBase):
    """Mock implementation of OpenAI service for testing purposes."""

    def open_client(self):
        pass

    def message(self, messages: List[dict]) -> OpenAiResponseModel:
        """Mock message method that returns predefined responses."""
        try:
            responses = [
                "I'm a mock AI assistant. I can help you with various tasks.",
                "This is a mock response. In production, you would get a real AI response.",
                "I'm simulating an AI response. Connect to OpenAI API for real interactions.",
                "Mock mode active. Switch to production mode to use actual AI capabilities."
            ]

            choices = [
                OpenAiChoiceModel(
                    message=OpenAiMessageModel(
                        content=random.choice(responses)
                    )
                )
            ]

            result: OpenAiResponseModel = OpenAiResponseModel(choices=choices)

            return result
        except Exception as e:
            print(f"Error in mock service: {str(e)}")
            raise
