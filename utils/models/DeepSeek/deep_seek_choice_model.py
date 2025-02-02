from pydantic import BaseModel
from utils.models.DeepSeek.deep_seek_message_model import DeepSeekMessageModel


class DeepSeekChoiceModel(BaseModel):

    message: DeepSeekMessageModel
