from utils.services.API.open_ai_service import OpenAiService


class DeepSeekConfig:

    def __init__(self, open_ai_service: OpenAiService):
        self.open_ai_service = open_ai_service
