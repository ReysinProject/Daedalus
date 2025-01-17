from typing import Callable, Literal

from daedalus.api.adapter.falcon_adapter import FalconAdapter
from daedalus.api.adapter.fastapi_adapter import FastAPIAdapter
from daedalus.api.adapter.framework_adapter import FrameworkAdapter

providers = {
    "falcon": FalconAdapter,
    "fastapi": FastAPIAdapter,
}


class DaedalusApiFactory:
    def __init__(self, framework: Literal["falcon", "fastapi"] = 'falcon'):
        self.adapter: FrameworkAdapter

        if framework not in providers:
            raise ValueError(f"Framework {framework} is not supported")

        self.adapter = providers[framework]()

    def route(self, path: str, methods: list[str]) -> Callable:
        return self.adapter.route(path, methods)

    def start(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        self.adapter.start(host, port)