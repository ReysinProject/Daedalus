from functools import wraps
from typing import Callable, TypeVar, Any
import inspect

T = TypeVar('T')


def search(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_query', True)
    setattr(wrapper, 'is_get', True)

    return wrapper