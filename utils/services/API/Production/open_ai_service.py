import openai
from injector import singleton
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
)

from Utils.Helpers.errors import OPEN_AI_ERRORS
from Utils.Models.OpenAI.openai_response_model import OpenAiResponseModel
from Utils.Models.OpenAI.openai_choice_model import OpenAiChoiceModel
from Utils.Models.OpenAI.openai_message_model import OpenAiMessageModel
from Utils.Models.OpenAI.user_message_model import UserMessageModel
from Utils.Services.ServiceLocator.configs.open_ai_config import OpenAIConfig
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase


@singleton
class OpenAiService(OpenAiServiceBase):

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.openai_client = self.__initialize_client()

    def __initialize_client(self):
        if (
            not self.config.ai_api_key
            or not self.config.base_api
            or not self.config.chat_model
        ):
            raise ValueError(
                "System variable 'BASE_API' or 'API_KEY' or 'CHAT_MODEL' is not set"
            )

        openai_client: openai.OpenAI = openai.OpenAI(
            api_key=self.config.ai_api_key, base_url=self.config.base_api
        )

        return openai_client

    def message(self, message: UserMessageModel) -> OpenAiResponseModel:

        try:
            messages = [
                ChatCompletionUserMessageParam(
                    role=message.role,
                    content=message.content,
                )
            ]

            response: ChatCompletion = self.openai_client.chat.completions.create(
                model=self.config.chat_model,
                messages=messages,
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
            error_message = getattr(e, "message", str(e))
            error_code = getattr(e, "code", "No code")
            raise ValueError(
                f"OpenAI Error - Message: {error_message}, Code: {error_code}"
            )

        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")
