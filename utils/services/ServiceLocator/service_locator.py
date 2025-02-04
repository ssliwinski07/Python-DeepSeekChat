import os
from injector import Injector, Module, provider, singleton

from utils.helpers.enums import ServiceType
from utils.services.ServiceLocator.configs.deep_seek_config import DeepSeekConfig
from utils.services.ServiceLocator.configs.open_ai_config import OpenAIConfig
from utils.services.API.open_ai_service import OpenAiService
from utils.consts.consts import DEEP_SEEK_API_KEY
from utils.services.production.DeepSeekService.deep_seek_service import (
    DeepSeekService,
)
from utils.services.mock.DeepSeekService.deep_seek_service_mock import (
    DeepSeekServiceMock,
)
from utils.services.base.deep_seek_service_base import DeepSeekServiceBase


class ServiceLocatorModule(Module):

    def __init__(
        self,
        open_ai_config: OpenAIConfig,
        deep_seek_config: DeepSeekConfig,
    ):
        self.open_ai_config = open_ai_config
        self.deep_seek_config = deep_seek_config

    def configure(self, binder):
        binder.bind(
            DeepSeekServiceBase,
            to=DeepSeekService(
                open_ai_service=self.deep_seek_config.open_ai_service,
            ),
            scope=singleton,
        )
        binder.bind(
            OpenAiService,
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
    def provide_deep_seek_service(self) -> DeepSeekServiceBase:
        return DeepSeekService(
            open_ai_service=self.deep_seek_config.open_ai_service,
        )

    @provider
    @singleton
    def provide_open_ai_service(self) -> OpenAiService:
        return OpenAiService(config=self.open_ai_config)

    @provider
    @singleton
    def provide_open_ai_config(self) -> OpenAIConfig:
        return self.open_ai_config

    @provider
    @singleton
    def provide_deep_seek_config(self) -> DeepSeekConfig:
        return self.deep_seek_config


class ServiceLocatorMockModule(Module):

    def configure(self, binder):
        binder.bind(DeepSeekServiceBase, to=DeepSeekServiceMock(), scope=singleton)

    @provider
    @singleton
    def provide_deep_seek_service_mock(self) -> DeepSeekServiceBase:
        return DeepSeekServiceMock()


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
        ai_api_key = os.getenv(DEEP_SEEK_API_KEY)

        open_ai_config: OpenAIConfig = OpenAIConfig(ai_api_key=ai_api_key)
        open_ai_service: OpenAiService = OpenAiService(config=open_ai_config)
        deep_seek_config: DeepSeekConfig = DeepSeekConfig(
            open_ai_service=open_ai_service
        )

        ### INJECTIONS PROD
        cls.__injector = Injector(
            ServiceLocatorModule(
                open_ai_config=open_ai_config,
                deep_seek_config=deep_seek_config,
            ),
            auto_bind=False,
        )

        ### INJECTIONS MOCK
        cls.__injector_mock = Injector(
            ServiceLocatorMockModule(),
            auto_bind=False,
        )
