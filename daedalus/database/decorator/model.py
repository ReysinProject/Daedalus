T = TypeVar('T')

def model(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_model', True)

    return wrapper