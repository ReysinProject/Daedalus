from daedalus.ioc.module import Module
from example.src.user.user_controller import UserController
from example.src.user.user_service import UserService


@Module()
class UserModule:
    imports = ['LoggerModule']
    providers = [UserService]
    controllers = [UserController]