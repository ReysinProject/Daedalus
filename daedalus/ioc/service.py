from daedalus.ioc.inject import Inject
from daedalus.ioc.injectable import Injectable


class Service:
    def __call__(self, cls):
        injectable = Injectable()

        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            for name, attr in cls.__dict__.items():
                if isinstance(attr, Inject):
                    setattr(instance, name, injectable.resolve_provider(attr.token))
            return instance

        wrapper.__name__ = cls.__name__
        return wrapper
