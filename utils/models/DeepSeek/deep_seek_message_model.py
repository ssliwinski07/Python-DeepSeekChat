from pydantic import BaseModel


class DeepSeekMessageModel(BaseModel):

    content: str
