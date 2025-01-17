from daedalus.ioc.controller import Controller
from daedalus.ioc.lazy_inject import LazyInject


@Controller()
class UserController:
    user_service = LazyInject('UserService')

    def create_user_route(self, username):
        self.user_service.create_user(username)
