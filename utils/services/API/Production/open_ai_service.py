import openai
from typing import List
from injector import singleton
from openai.types.chat import ChatCompletion

from Utils.Helpers.errors import OPEN_AI_ERRORS
from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel
from Utils.Models.OpenAI.openai_choice_model import OpenAiChoiceModel
from Utils.Models.OpenAI.openai_message_model import OpenAiMessageModel
from Utils.Services.ServiceLocator.configs.open_ai_config import OpenAIConfig
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase


@singleton
class OpenAiService(OpenAiServiceBase):

    def __init__(self, config: OpenAIConfig):
        self.config = config

    __client: openai.OpenAI = None

    def open_client(self):
        if not self.__client:
            if (
                not self.config.ai_api_key
                or not self.config.base_api
                or not self.config.chat_model
            ):
                raise ValueError(
                    "System variable 'BASE_API' or 'API_KEY' or 'CHAT_MODEL' is not set"
                )

            self.__client = openai.OpenAI(
                api_key=self.config.ai_api_key, base_url=self.config.base_api
            )

    def message(self, messages: List[dict]) -> OpenAiResponseModel:

        self.open_client()

        try:
            response: ChatCompletion = self.__client.chat.completions.create(
                model=self.config.chat_model,
                messages=messages,
                stream=False,
            )

            choices = [
                OpenAiChoiceModel(
                    message=OpenAiMessageModel(content=choice.message.content)
                )
                for choice in response.choices
            ]

            result: OpenAiResponseModel = OpenAiResponseModel(choices=choices)

            return result
        except OPEN_AI_ERRORS as e:
            raise ValueError(f"{e.body['message']}, code: {e.body['code']}")

        except Exception as e:
            raise ValueError(f"{e}")
