from Utils.Models.DeepSeek.user_message_model import UserMessageModel
from Utils.Models.DeepSeek.deep_seek_response_model import DeepSeekResponseModel
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Consts.consts import USER_ROLE


class OpenAiChatVM:

    def __init__(
        self,
        open_ai_service: OpenAiServiceBase,
    ):
        self.open_ai_service = open_ai_service

    def start_chat(self):
        print("OpenAi: type 'exit' to end the conversation")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print("See ya!")
                break

            user_msg: UserMessageModel = UserMessageModel(
                role=USER_ROLE, content=user_input
            )

            messages = []

            messages.append(user_msg.model_dump())

            reply: DeepSeekResponseModel = self.open_ai_service.message(
                messages=messages
            )

            print(f"OpenAi: {reply.choices[0].message.content}")
