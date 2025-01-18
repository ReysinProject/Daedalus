from functools import wraps
from typing import Callable


def endpoint(path: str = "/", methods: list[str] = ["GET"]):
    """
    Route decorator that preserves the class instance context.
    Args:
        path (str): The path of the route
        methods (list[str]): The methods of the route
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        wrapper._route = {
            'path': path,
            'methods': methods,
            'handler': wrapper
        }
        return wrapper

    return decorator