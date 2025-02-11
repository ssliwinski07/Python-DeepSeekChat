from pydantic import BaseModel
from Utils.Models.OpenAI.openai_message_model import OpenAiMessageModel


class OpenAiChoiceModel(BaseModel):
    message: OpenAiMessageModel
