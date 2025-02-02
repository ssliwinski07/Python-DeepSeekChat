import os

from utils.services.API.DeepSeekService.deep_seek_service import DeepSeekService
from utils.view_models.deep_seek_vm import DeepSeekVM


def main():

    try:
        ai_token = os.getenv("AI_TOKEN")
        deep_seek_service: DeepSeekService = DeepSeekService(ai_token=ai_token)

        deep_seek_vm: DeepSeekVM = DeepSeekVM(deep_seek_service=deep_seek_service)

        deep_seek_vm.start_chat()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
