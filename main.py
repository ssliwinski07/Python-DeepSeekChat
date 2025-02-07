from Utils.Helpers.enums import ServiceType
from Utils.Services.ServiceLocator.service_locator import ServicesInjector
from Utils.ViewModels.deep_seek_vm import DeepSeekVM
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase


def main():

    try:
        ServicesInjector.init()

        # Based on service_type parameter the right module is picked up to search in for the service to be returned
        # For example when passing ServiceType.MOCK/ServiceType.PRODUCTION, ServicesInjector will search in ServiceLocatorMockModule/ServiceLocatorModule
        # You can pass the base class name to get() function since it's implementations are mapped to base class in the module that is picked based on service_type parameter from ServicesInjector.injector()
        # In that case, since service_type = ServiceType.PRODUCTION, injector will get DeepSeekService
        # If you want to test the program and get generic replies (if you don't have api key from DeepSeek), you need to change service_type parameter to ServiceType.MOCK
        injector = ServicesInjector.injector(service_type=ServiceType.PRODUCTION)

        open_ai_service = injector.get(OpenAiServiceBase)

        deep_seek_vm: DeepSeekVM = DeepSeekVM(
            open_ai_service=open_ai_service,
        )

        deep_seek_vm.start_chat()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
