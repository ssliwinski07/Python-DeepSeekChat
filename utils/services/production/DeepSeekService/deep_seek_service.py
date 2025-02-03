import openai
from openai.types.chat import ChatCompletion
from typing import List
from injector import singleton

from utils.consts.consts import BASE_API, DEEP_SEEK_CHAT_MODEL
from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from utils.services.ServiceLocator.configs.deep_seek_config import DeepSeekConfig
from utils.services.base.deep_seek_service_base import DeepSeekServiceBase
from utils.services.API.open_ai_service import OpenAiService


@singleton
class DeepSeekService(DeepSeekServiceBase):

    def __init__(self, open_ai_service: OpenAiService):
        self.open_ai_service = open_ai_service

    def send_msg(self, messages: List[dict]) -> DeepSeekResponseModel:
        try:
            result: DeepSeekResponseModel = self.open_ai_service.message(
                messages=messages
            )

            return result
        except Exception as e:
            raise ValueError(f"{e}")
