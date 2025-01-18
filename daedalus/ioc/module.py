class Module:
    def __call__(self, cls):
        setattr(cls, '__decorated__', True)
        return cls
