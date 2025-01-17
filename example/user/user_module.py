from daedalus.ioc.module import Module
from example.user.user_controller import UserController
from example.user.user_service import UserService


@Module()
class UserModule:
    imports = ['LoggerModule']
    providers = [UserService]
    controllers = [UserController]