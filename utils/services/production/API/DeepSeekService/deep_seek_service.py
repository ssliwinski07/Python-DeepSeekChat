import openai
from openai.types.chat import ChatCompletion
from typing import List
from injector import singleton

from utils.consts.consts import BASE_API, DEEP_SEEK_CHAT_MODEL
from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from utils.services.ServiceLocator.configs.deep_seek_config import DeepSeekConfig
from utils.services.base.deep_seek_service_base import DeepSeekServiceBase


@singleton
class DeepSeekService(DeepSeekServiceBase):

    def __init__(self, config: DeepSeekConfig):
        self.config = config
        self.client: openai.OpenAI = None

        self.open_client()

    def open_client(self):
        if not self.client:
            if not self.config.ai_token:
                raise ValueError("system variable with token is not set")

            self.client = openai.OpenAI(api_key=self.config.ai_token, base_url=BASE_API)

    def send_msg(self, messages: List[dict]) -> DeepSeekResponseModel:

        try:
            response: ChatCompletion = self.client.chat.completions.create(
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
