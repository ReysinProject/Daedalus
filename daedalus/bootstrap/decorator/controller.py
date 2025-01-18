class Controller:
    def __call__(self, cls):
        setattr(cls, '__decorated__', True)
        setattr(cls, 'is_controller', True)
        return cls
