from typing import Any, Callable

from daedalus.api.adapter.framework_adapter import FrameworkAdapter
from daedalus.api.interface.request import Request
from daedalus.api.interface.response import Response


class FastAPIAdapter(FrameworkAdapter):
    def __init__(self):
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
        self.app = FastAPI()
        self._request_class = Request
        self._response_class = JSONResponse

    def route(self, path: str, methods: list[str]) -> Callable:
        def decorator(handler: Callable) -> Callable:
            @self.app.api_route(path, methods=methods)
            async def wrapper(request: self._request_class):
                janus_request = await self.convert_request(request)
                janus_response = handler(janus_request, **request.path_params)
                return self.convert_response(janus_response)
            return wrapper
        return decorator

    def start(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

    async def convert_request(self, framework_request: Any) -> Request:
        try:
            body = await framework_request.json()
        except:
            body = {}

        return Request(
            method=framework_request.method,
            path=framework_request.url.path,
            headers=dict(framework_request.headers),
            body=body,
            query_params=dict(framework_request.query_params)
        )

    def convert_response(self, janus_response: Response) -> Any:
        return self._response_class(
            content=janus_response.data,
            status_code=janus_response.status_code,
            headers=janus_response.headers
        )