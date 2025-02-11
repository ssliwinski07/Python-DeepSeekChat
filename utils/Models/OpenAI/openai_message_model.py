from pydantic import BaseModel


class OpenAiMessageModel(BaseModel):
    content: str
