from typing import Dict, Any


class Request:
    def __init__(self, method: str, path: str, headers: Dict, body: Any, query_params: Dict):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.query_params = query_params