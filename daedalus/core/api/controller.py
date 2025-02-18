from typing import Callable
from daedalus.core.api.context.controller_context import ControllerContext

class Controller:
    def __init__(self, prefix: str = None, access_limitation: Callable[[ControllerContext], bool] = lambda _: True):
        self.prefix = prefix
        self.access_limitation = access_limitation

    def __call__(self, cls):
        prefix = self.prefix
        access_limitation = self.access_limitation

        # Attribute for the bootstrapper to identify the class as a controller
        setattr(cls, '__decorated__', True)
        setattr(cls, 'is_controller', True)

        # Save the original __init__ method
        original_init = cls.__init__

        # Define a new __init__ method
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            setattr(self, 'container', "test")
            setattr(self, 'prefix', prefix)
            setattr(self, 'access_limitation', access_limitation)

        # Replace the original __init__ method with the new one
        cls.__init__ = new_init

        return cls
