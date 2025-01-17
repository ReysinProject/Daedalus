import json
from typing import Callable, Any

from daedalus.api.adapter.framework_adapter import FrameworkAdapter
from daedalus.api.interface.request import JanusRequest
from daedalus.api.interface.response import JanusResponse


class FalconAdapter(FrameworkAdapter):
    def __init__(self):
        import falcon
        self.app = falcon.App()
        self._response_class = falcon.Response

    def route(self, path: str, methods: list[str]) -> Callable:
        def decorator(handler: Callable) -> Callable:
            class Resource:
                def __init__(self, handler):
                    self.handler = handler

                def on_get(self, req, resp, **kwargs):
                    if 'GET' not in methods:
                        from falcon import HTTP_405
                        resp.status = HTTP_405
                        return
                    self._handle_request('GET', req, resp, **kwargs)

                def on_post(self, req, resp, **kwargs):
                    if 'POST' not in methods:
                        from falcon import HTTP_405
                        resp.status = HTTP_405
                        return
                    self._handle_request('POST', req, resp, **kwargs)

                def _handle_request(self, method, req, resp, **kwargs):
                    janus_request = self.convert_request(req)
                    janus_response = handler(janus_request, **kwargs)
                    self.convert_response(janus_response, resp)

                def convert_request(self, req) -> JanusRequest:
                    try:
                        body = json.load(req.stream)
                    except:
                        body = {}

                    return JanusRequest(
                        method=req.method,
                        path=req.path,
                        headers=req.headers,
                        body=body,
                        query_params=req.params
                    )

                def convert_response(self, janus_response: JanusResponse, resp: Any) -> None:
                    resp.text = json.dumps(janus_response.data)
                    resp.status = str(janus_response.status_code)
                    resp.content_type = 'application/json'
                    for key, value in janus_response.headers.items():
                        resp.set_header(key, value)

            self.app.add_route(path, Resource(handler))
            return handler

        return decorator

    def start(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        import waitress
        waitress.serve(self.app, host=host, port=port)

    def convert_request(self, framework_request: Any) -> JanusRequest:
        # This method is implemented in the Resource class
        pass

    def convert_response(self, janus_response: JanusResponse) -> Any:
        # This method is implemented in the Resource class
        pass
