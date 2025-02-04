import openai
from typing import List
from injector import singleton
from openai.types.chat import ChatCompletion

from Utils.Models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from Utils.Services.ServiceLocator.configs.open_ai_config import OpenAIConfig
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Consts.consts import BASE_API, DEEP_SEEK_CHAT_MODEL


@singleton
class OpenAiService(OpenAiServiceBase):

    def __init__(self, config: OpenAIConfig):
        self.config = config

    __client: openai.OpenAI = None

    def open_client(self):
        if not self.__client:
            if not self.config.ai_api_key:
                raise ValueError("system variable with token is not set")

            self.__client = openai.OpenAI(
                api_key=self.config.ai_api_key, base_url=BASE_API
            )

    def message(self, messages: List[dict]) -> DeepSeekResponseModel:

        self.open_client()

        try:
            response: ChatCompletion = self.__client.chat.completions.create(
                model=DEEP_SEEK_CHAT_MODEL,
                messages=messages,
                stream=False,
            )

            ##choices = [DeepSeekChoiceModel(**choice) for choice in response.choices]

            result: DeepSeekResponseModel = DeepSeekResponseModel(
                choices=response.choices
            )

            return result
        except (
            openai.AuthenticationError,
            openai.BadRequestError,
            openai.RateLimitError,
            openai.APIConnectionError,
        ) as e:
            raise ValueError(f"{e.body['message']}")

        except Exception as e:
            raise ValueError(f"{e}")
