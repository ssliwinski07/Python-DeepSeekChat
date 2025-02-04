from pydantic import BaseModel

from Utils.Models.DeepSeek.deep_seek_message_model import DeepSeekMessageModel


class DeepSeekChoiceModel(BaseModel):

    message: DeepSeekMessageModel
