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
            DeepSeekService,
            to=DeepSeekService(open_ai_service=self.deep_seek_config.open_ai_service),
            scope=singleton,
        )

    @provider
    @singleton
    def provide_deep_seek_service(self) -> DeepSeekService:
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
        binder.bind(DeepSeekServiceMock, to=DeepSeekServiceMock(), scope=singleton)

    @provider
    @singleton
    def provide_deep_seek_service_mock(self) -> DeepSeekServiceMock:
        return DeepSeekServiceMock()


class ServicesInjector:

    __injector: Injector = None
    __injector_mock: Injector = None

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
