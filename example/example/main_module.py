from daedalus.bootstrap.decorator.module import Module


@Module()
class MainModule:
    providers = []
    controllers = []
    imports = ['CountModule']
