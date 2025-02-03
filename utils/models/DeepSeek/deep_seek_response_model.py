from pydantic import BaseModel
from typing import List
from openai.types.chat.chat_completion import Choice
from utils.models.DeepSeek.deep_seek_choice_model import DeepSeekChoiceModel


class DeepSeekResponseModel(BaseModel):

    choices: List[DeepSeekChoiceModel]
