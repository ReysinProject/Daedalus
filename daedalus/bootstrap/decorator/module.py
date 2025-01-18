class Module:
    def __call__(self, cls):
        setattr(cls, '__decorated__', True)
        setattr(cls, 'is_module', True)
        return cls
