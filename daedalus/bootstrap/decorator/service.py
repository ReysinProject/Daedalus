class Service:
    def __call__(self, cls):
        setattr(cls, '__decorated__', True)
        setattr(cls, 'is_service', True)
        return cls
