from typing import List
from injector import singleton

from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from utils.services.base.deep_seek_service_base import DeepSeekServiceBase
from utils.models.DeepSeek.deep_seek_choice_model import DeepSeekChoiceModel
from utils.models.DeepSeek.deep_seek_message_model import DeepSeekMessageModel


@singleton
class DeepSeekServiceMock(DeepSeekServiceBase):

    def open_client(self):
        return

    def send_msg(self, messages: List[dict]) -> DeepSeekResponseModel:

        try:
            choices = [
                DeepSeekChoiceModel(message=DeepSeekMessageModel(content="Hi there")),
            ]

            result: DeepSeekResponseModel = DeepSeekResponseModel(choices=choices)

            return result
        except Exception as e:
            raise ValueError(f"{e}")
