class OpenAIConfig:

    def __init__(
        self,
        ai_api_key: str,
        chat_model: str,
        base_api: str,
    ):
        self.ai_api_key = ai_api_key
        self.chat_model = chat_model
        self.base_api = base_api
