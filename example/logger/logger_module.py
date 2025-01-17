from daedalus.ioc.module import Module
from example.logger.logger_service import LoggerService


@Module()
class LoggerModule:
    providers = [LoggerService]
    controllers = []
    imports = []
