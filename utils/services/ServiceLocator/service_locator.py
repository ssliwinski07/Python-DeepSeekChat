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
        service_type: ServiceType = ServiceType.PRODUCTION,
    ):
        self.service_type = service_type
        self.open_ai_config = open_ai_config

    @singleton
    @provider
    def provide_deep_seek_service(
        self, open_ai_service: OpenAiService
    ) -> DeepSeekService:
        match self.service_type:
            case ServiceType.PRODUCTION:
                return DeepSeekService(open_ai_service=open_ai_service)
            case ServiceType.MOCK:
                return DeepSeekServiceMock()

    @singleton
    @provider
    def provide_open_ai_service(self) -> OpenAiService:
        return OpenAiService(config=self.open_ai_config)

    @singleton
    @provider
    def provide_open_ai_config(self) -> OpenAIConfig:
        return self.open_ai_config


class ServicesInjector:

    __injector: Injector = None
    __injector_mock: Injector = None

    @classmethod
    def injector(cls) -> Injector:
        if not cls.__injector:
            raise ValueError(
                "Injector for production has not been initialized. Call init() before using it."
            )
        return cls.__injector

    @classmethod
    def injector_mock(cls) -> Injector:
        if not cls.__injector_mock:
            raise ValueError(
                "Injector for mock has not been initialized. Call init() before using it."
            )
        return cls.__injector_mock

    @classmethod
    def init(cls):

        ### CONFIGS
        ai_api_key = os.getenv(DEEP_SEEK_API_KEY)
        open_ai_config: OpenAIConfig = OpenAIConfig(ai_api_key=ai_api_key)

        ### INJECTIONS PROD
        cls.__injector = Injector(
            ServiceLocatorModule(
                open_ai_config=open_ai_config,
            ),
        )

        ### INJECTIONS MOCK
        cls.__injector_mock = Injector(
            ServiceLocatorModule(
                service_type=ServiceType.MOCK, open_ai_config=open_ai_config
            ),
        )
