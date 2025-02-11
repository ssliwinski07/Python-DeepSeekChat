from pydantic import BaseModel
from typing import List
from Utils.Models.OpenAI.openai_choice_model import OpenAiChoiceModel


class OpenAiResponseModel(BaseModel):
    choices: List[OpenAiChoiceModel]
