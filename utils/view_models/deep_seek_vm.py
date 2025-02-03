from utils.services.production.API.DeepSeekService.deep_seek_service import (
    DeepSeekService,
)
from utils.models.DeepSeek.user_message_model import UserMessageModel
from utils.models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from utils.consts.consts import USER_ROLE


class DeepSeekVM:

    def __init__(self, deep_seek_service: DeepSeekService):
        self.deep_seek_service = deep_seek_service

    def start_chat(self):
        print("DeepSeek: type 'exit deepseek' to end the conversation")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit deepseek":
                print("See ya!")
                break

            user_msg: UserMessageModel = UserMessageModel(
                role=USER_ROLE, content=user_input
            )

            messages = []

            messages.append(user_msg.model_dump())

            reply: DeepSeekResponseModel = self.deep_seek_service.send_msg(
                messages=messages
            )

            print(f"DeepSeek: {reply.choices[0].message.content}")
