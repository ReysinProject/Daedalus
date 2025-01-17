from daedalus.ioc.injectable import Injectable
from logger.logger_module import LoggerModule
from user.user_module import UserModule
from user.user_controller import UserController

# Register modules
injectable = Injectable()
injectable.register_module(LoggerModule.__name__, LoggerModule())
injectable.register_module(UserModule.__name__, UserModule())

# Resolve dependencies
user_controller = injectable.resolve_provider(UserController.__name__)
user_controller.create_user_route("john_doe")