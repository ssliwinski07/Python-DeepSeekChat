from pydantic import BaseModel
from typing import Optional


class OpenAiMessageModel(BaseModel):
    content: Optional[str] = None
