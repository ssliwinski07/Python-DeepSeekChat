import openai
from openai.types.chat import ChatCompletion
from typing import List

from utils.consts.consts import BASE_API, DEEP_SEEK_CHAT_MODEL
from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel


class DeepSeekService:

    _instance = None

    # making class as a singleton, to be sure service is initialized only once
    def __new__(cls, ai_token):
        if cls._instance is None:
            cls._instance = super(DeepSeekService, cls).__new__(cls)
            cls._instance._init(ai_token)

        return cls._instance

    def _init(self, ai_token):
        self.ai_token = ai_token
        self.client: openai.OpenAI = None

        self.open_client()

    def open_client(self):
        if not self.client:
            if not self.ai_token:
                raise ValueError("system variable with token is not set")

            self.client = openai.OpenAI(api_key=self.ai_token, base_url=BASE_API)

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
