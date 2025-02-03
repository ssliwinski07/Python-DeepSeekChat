from typing import List
from injector import singleton
import random

from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from utils.services.base.deep_seek_service_base import DeepSeekServiceBase
from utils.models.DeepSeek.deep_seek_choice_model import DeepSeekChoiceModel
from utils.models.DeepSeek.deep_seek_message_model import DeepSeekMessageModel


@singleton
class DeepSeekServiceMock(DeepSeekServiceBase):

    def send_msg(self, messages: List[dict]) -> DeepSeekResponseModel:

        content = [
            "You're awesome",
            "Hi, there!",
            "I'm potato",
            "Empty shell",
            "Gosia is beautiful",
            "Cats are cool",
        ]
        random_number = random.randint(0, len(content) - 1)

        try:
            choices = [
                DeepSeekChoiceModel(
                    message=DeepSeekMessageModel(
                        content=content[random_number],
                    )
                ),
            ]

            result: DeepSeekResponseModel = DeepSeekResponseModel(choices=choices)

            return result
        except Exception as e:
            raise ValueError(f"{e}")
