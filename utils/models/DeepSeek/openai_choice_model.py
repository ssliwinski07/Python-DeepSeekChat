from pydantic import BaseModel
from Utils.Models.DeepSeek.openai_message_model import OpenAiMessageModel


class OpenAiChoiceModel(BaseModel):
    message: OpenAiMessageModel
