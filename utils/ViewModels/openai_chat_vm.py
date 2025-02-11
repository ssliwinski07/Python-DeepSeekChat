from Utils.Models.DeepSeek.user_message_model import UserMessageModel
from Utils.Models.DeepSeek.openai_response_model import OpenAiResponseModel
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Consts.consts import USER_ROLE
from typing import List


class OpenAiChatVM:
    def __init__(
        self,
        open_ai_service: OpenAiServiceBase,
    ):
        self.open_ai_service = open_ai_service
        self.conversation_history: List[dict] = []

    def start_chat(self):
        print("OpenAi: type 'exit' to end the conversation")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "exit":
                    print("See ya!")
                    break

                user_msg: UserMessageModel = UserMessageModel(
                    role=USER_ROLE, content=user_input
                )

                # Add user message to history
                self.conversation_history.append(user_msg.model_dump())

                try:
                    reply: OpenAiResponseModel = self.open_ai_service.message(
                        messages=self.conversation_history
                    )

                    assistant_message = reply.choices[0].message.content
                    print(f"OpenAi: {assistant_message}")

                    # Add assistant's reply to history
                    self.conversation_history.append(
                        reply.choices[0].message.model_dump()
                    )

                except Exception as api_error:
                    print(f"Error getting response from OpenAI: {api_error}")
                    print("Please try again or type 'exit' to quit.")

            except KeyboardInterrupt:
                print("\nChat session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again or type 'exit' to quit.")
