class Injectable:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Injectable, cls).__new__(cls)
            cls._instance._providers = {}
            cls._instance._modules = {}
        return cls._instance

    def register_provider(self, token, cls):
        print(token)
        self._providers[token] = cls

    def register_module(self, token, module):
        self._modules[token] = module

    def resolve_provider(self, token):
        cls = self._providers.get(token)
        if cls is None:
            for key in self._providers.keys():
                print(key)
            raise ValueError(f"No provider found for token: {token}")
        return cls()

    def resolve_module(self, token):
        module = self._modules.get(token)
        if module is None:
            raise ValueError(f"No module found for token: {token}")
        return module