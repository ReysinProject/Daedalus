from typing import Any, Optional, Dict


class JanusResponse:
    def __init__(self, data: Any, status_code: int = 200, headers: Optional[Dict] = None):
        self.data = data
        self.status_code = status_code
        self.headers = headers or {}