from pydantic import BaseModel
from typing_extensions import Literal


class UserMessageModel(BaseModel):
    role: Literal["user"]
    content: str
