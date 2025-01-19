from daedalus.bootstrap.decorator.module import Module


@Module()
class CountModule:
    imports = []
    providers = ['CountService']
    controllers = ['CountController']