from typing import Callable



def endpoint(path: str = "/", methods: list[str] = ["GET"]):
    """
    Route decorator.

    Args:
        path (str): The path of the route
        methods (list[str]): The methods of the route
    """
    def decorator(func: Callable):
        func._route = {
            'path': path,
            'methods': methods,
            'handler': func
        }
        return func
    return decorator