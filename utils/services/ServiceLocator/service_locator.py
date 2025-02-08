import os
from injector import Injector, Module, provider, singleton

from Utils.Helpers.enums import ServiceType
from Utils.Services.ServiceLocator.configs.open_ai_config import OpenAIConfig
from Utils.Services.API.Production.open_ai_service import OpenAiService
from Utils.Consts.consts import API_KEY, CHAT_MODEL, BASE_API
from Utils.Services.API.Base.open_ai_service_base import OpenAiServiceBase
from Utils.Services.API.Mock.open_ai_service_mock import OpenAiServiceMock


class ServiceLocatorModule(Module):

    def __init__(
        self,
        open_ai_config: OpenAIConfig,
    ):
        self.open_ai_config = open_ai_config

    def configure(self, binder):
        binder.bind(
            OpenAiServiceBase,
            to=OpenAiService(
                config=self.open_ai_config,
            ),
            scope=singleton,
        )

    # here we can map DeepSeekServiceBase (which is an interface) to DeepSeekService
    # thanks to that when getting the service, we can pass the interface class name instead of class that implements it
    # that's helpful when working with production services and mock services for tests - you don't need to change the name on the class when getting the service since both services are mapped to the base class
    # look at the provide_deep_seek_service_mock in ServiceLocatorMockModule - it's also mapped with base class
    @provider
    @singleton
    def provide_open_ai_service(self) -> OpenAiServiceBase:
        return OpenAiService(config=self.open_ai_config)

    @provider
    @singleton
    def provide_open_ai_config(self) -> OpenAIConfig:
        return self.open_ai_config


class ServiceLocatorMockModule(Module):

    def configure(self, binder):
        binder.bind(OpenAiServiceBase, to=OpenAiServiceMock(), scope=singleton)

    @provider
    @singleton
    def provide_deep_seek_service_mock(self) -> OpenAiServiceBase:
        return OpenAiServiceMock()


class ServicesInjector:

    __injector: Injector = None
    __injector_mock: Injector = None

    # thanks to service_type we can choose the right module (ServiceLocatorMockModule or ServiceLocatorModule) to look for services during getting them.
    @classmethod
    def injector(cls, service_type: ServiceType) -> Injector:
        match service_type:
            case ServiceType.PRODUCTION:
                if not cls.__injector:
                    raise ValueError(
                        "Injector for production has not been initialized. Call ServicesInjector.init() before using it."
                    )
                return cls.__injector
            case ServiceType.MOCK:
                if not cls.__injector_mock:
                    raise ValueError(
                        "Injector for mock has not been initialized. Call ServicesInjector.init() before using it."
                    )
                return cls.__injector_mock

    @classmethod
    def init(cls):
        ### CONFIGS/SERVICES
        ai_api_key: str = os.getenv(API_KEY)
        chat_model: str = os.getenv(CHAT_MODEL)
        base_api: str = os.getenv(BASE_API)

        open_ai_config: OpenAIConfig = OpenAIConfig(
            ai_api_key=ai_api_key,
            chat_model=chat_model,
            base_api=base_api,
        )

        ### INJECTIONS PROD
        cls.__injector = Injector(
            ServiceLocatorModule(
                open_ai_config=open_ai_config,
            ),
            auto_bind=False,
        )

        ### INJECTIONS MOCK
        cls.__injector_mock = Injector(
            ServiceLocatorMockModule(),
            auto_bind=False,
        )
