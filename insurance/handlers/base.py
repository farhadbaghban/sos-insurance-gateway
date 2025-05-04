from typing import Any

from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self, raw_data: dict):
        self.raw_data = raw_data

    @abstractmethod
    def parse(self) -> None:
        pass

    @abstractmethod
    def save(self) -> Any:
        pass


class CompanyHandlerFactory:
    _handlers = {}

    @classmethod
    def register_handler(cls, company_id: str, handler_cls):
        cls._handlers[company_id] = handler_cls

    @classmethod
    def get_handler(cls, company_id: str):
        if company_id not in cls._handlers:
            raise ValueError(f"Unsupported company ID: {company_id}")
        return cls._handlers[company_id]