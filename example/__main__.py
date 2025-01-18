from daedalus.core.factory import DaedalusFactory
from example.src.main_module import MainModule

app = DaedalusFactory(MainModule)

app.serve()

# # Register modules
# injectable = Injectable()
# injectable.register_module(LoggerModule.__name__, LoggerModule())
# injectable.register_module(UserModule.__name__, UserModule())
#
# # Resolve dependencies
# user_controller = injectable.resolve_provider(UserController.__name__)
# user_controller.create_user_route("john_doe")