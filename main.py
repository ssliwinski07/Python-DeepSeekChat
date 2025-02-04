from utils.helpers.enums import ServiceType
from utils.services.production.DeepSeekService.deep_seek_service import (
    DeepSeekService,
)
from utils.services.mock.DeepSeekService.deep_seek_service_mock import (
    DeepSeekServiceMock,
)
from utils.services.ServiceLocator.service_locator import ServicesInjector
from utils.view_models.deep_seek_vm import DeepSeekVM


def main():

    try:
        ServicesInjector.init()

        # injector for getting prod/mock services, pass ServiceType.MOCK or ServiceType.PRODUCTION to initalize get injector
        injector = ServicesInjector.injector(service_type=ServiceType.PRODUCTION)

        # based on injector type (production/mock) pass DeepSeekService or DeepSeekServiceMock as a parameter of get function
        deep_seek_service = injector.get(DeepSeekService)

        deep_seek_vm: DeepSeekVM = DeepSeekVM(deep_seek_service=deep_seek_service)

        deep_seek_vm.start_chat()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
