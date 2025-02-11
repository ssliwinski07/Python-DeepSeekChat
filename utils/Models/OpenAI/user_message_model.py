from pydantic import BaseModel


class UserMessageModel(BaseModel):

    role: str
    content: str
