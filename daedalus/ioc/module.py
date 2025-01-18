import inspect
import os

from daedalus.ioc.injectable import Injectable


class Module:
    def __call__(self, cls):
        injectable = Injectable()
        module_instance = cls()
        injectable.register_module(cls.__name__, module_instance)

        setattr(cls, '__decorated__', True)
        setattr(cls, '__module_type__', 'module')

        # Register providers and controllers from imported modules
        for import_module in module_instance.imports:
            imported_module = injectable.resolve_module(import_module)
            for provider in imported_module.providers:
                injectable.register_provider(provider.__name__, provider)
            for controller in imported_module.controllers:
                injectable.register_provider(controller.__name__, controller)

        # Register providers and controllers from the current module
        for provider in module_instance.providers:
            injectable.register_provider(provider.__name__, provider)
        for controller in module_instance.controllers:
            injectable.register_provider(controller.__name__, controller)

        return cls
