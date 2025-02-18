from functools import wraps
from typing import Callable, TypeVar, Any
import inspect

T = TypeVar('T')


def mutate(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    # Store metadata for the bootstrapper
    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_mutate', True)
    setattr(wrapper, 'original_func', func)

    # Store the signature for GraphQL schema generation
    signature = inspect.signature(func)
    setattr(wrapper, 'signature', signature)

    return wrapper
