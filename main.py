from injector import Injector

from utils.services.production.API.DeepSeekService.deep_seek_service import (
    DeepSeekService,
)
from utils.services.mock.API.DeepSeekService.deep_seek_service_mock import (
    DeepSeekServiceMock,
)
from utils.services.ServiceLocator.service_locator import ServicesInjector
from utils.view_models.deep_seek_vm import DeepSeekVM


def main():

    try:
        ServicesInjector.init()

        ### injector for prod service
        injector = ServicesInjector.injector()
        deep_seek_service = injector.get(DeepSeekService)

        ### injector for mock service
        # injector_mock: Injector = ServicesInjector.injector_mock()
        # deep_seek_service = injector_mock.get(DeepSeekServiceMock)

        deep_seek_vm: DeepSeekVM = DeepSeekVM(deep_seek_service=deep_seek_service)

        deep_seek_vm.start_chat()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
