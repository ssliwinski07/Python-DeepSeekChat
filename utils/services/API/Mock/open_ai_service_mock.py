from typing import List
import random

from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from Utils.Models.DeepSeek.deep_seek_choice_model import DeepSeekChoiceModel
from Utils.Models.DeepSeek.deep_seek_message_model import DeepSeekMessageModel


class OpenAiServiceMock(OpenAiServiceBase):

    def open_client(self):
        return None

    def message(self, messages: List[dict]) -> DeepSeekResponseModel:

        content = (
            [
                "You're awesome",
                "Hi, there!",
                "I'm potato",
                "Empty shell",
                "Gosia is beautiful",
                "Cats are cool",
            ]
            if messages is not None
            else ["Generic reply"]
        )

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
