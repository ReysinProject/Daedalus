from abc import ABC, abstractmethod
from typing import Callable, Any

from daedalus.api.interface.request import Request
from daedalus.api.interface.response import Response


class FrameworkAdapter(ABC):
    @abstractmethod
    def route(self, path: str, methods: list[str]) -> Callable:
        pass

    @abstractmethod
    def start(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        pass

    @abstractmethod
    def convert_request(self, framework_request: Any) -> Request:
        pass

    @abstractmethod
    def convert_response(self, janus_response: Response) -> Any:
        pass