from pydantic import BaseModel
from typing import List

from utils.models.DeepSeek.deep_seek_choice_model import DeepSeekChoiceModel


class DeepSeekResponseModel(BaseModel):

    choices: List[DeepSeekChoiceModel]
