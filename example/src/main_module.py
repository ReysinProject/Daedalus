from daedalus.bootstrap.decorator.module import Module


@Module()
class MainModule:
    providers = []
    controllers = []
    imports = ['UserModule', 'LoggerModule', 'TestModule']
