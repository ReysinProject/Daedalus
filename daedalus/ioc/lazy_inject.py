from daedalus.ioc.injectable import Injectable


class LazyInject:
    def __init__(self, token):
        self.token = token

    def __get__(self, instance, owner):
        injectable = Injectable()
        return injectable.resolve_provider(self.token)