import os
from injector import Injector, Module, provider, singleton

from utils.helpers.enums import ServiceType
from utils.services.ServiceLocator.configs.deep_seek_config import DeepSeekConfig
from utils.services.production.API.DeepSeekService.deep_seek_service import (
    DeepSeekService,
)
from utils.services.mock.API.DeepSeekService.deep_seek_service_mock import (
    DeepSeekServiceMock,
)


class ServiceLocatorModule(Module):

    def __init__(
        self,
        deep_seek_config: DeepSeekConfig,
        service_type: ServiceType = ServiceType.PRODUCTION,
    ):
        self.service_type = service_type
        self.deep_seek_config = deep_seek_config

    @singleton
    @provider
    def provide_deep_seek_service(self, config: DeepSeekConfig) -> DeepSeekService:
        match self.service_type:
            case ServiceType.PRODUCTION:
                return DeepSeekService(config)
            case ServiceType.MOCK:
                return DeepSeekServiceMock()

    @singleton
    @provider
    def provide_deep_seek_config(self) -> DeepSeekConfig:
        return self.deep_seek_config


class ServicesInjector:

    _injector: Injector = None
    _injector_mock: Injector = None

    @classmethod
    def injector(cls) -> Injector:
        if not cls._injector:
            raise ValueError(
                "Injector for production has not been initialized. Call init() before using it."
            )
        return cls._injector

    @classmethod
    def injector_mock(cls) -> Injector:
        if not cls._injector_mock:
            raise ValueError(
                "Injector for mock has not been initialized. Call init() before using it."
            )
        return cls._injector_mock

    @classmethod
    def init(cls):

        ### DEEP SEEK CONFIG
        ai_token = os.getenv("AI_TOKEN")
        deep_seek_config: DeepSeekConfig = DeepSeekConfig(ai_token=ai_token)

        ### INJECTIONS PROD
        cls._injector = Injector(
            ServiceLocatorModule(
                deep_seek_config=deep_seek_config,
            ),
        )

        ### INJECTIONS MOCK
        cls._injector_mock = Injector(
            ServiceLocatorModule(
                deep_seek_config=deep_seek_config,
                service_type=ServiceType.MOCK,
            ),
        )
