from daedalus.bootstrap.decorator.controller import Controller
from example.src.user.user_service import UserService


@Controller()
class UserController:
    inject = ['UserService']

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user_route(self, username):
        self.user_service.create_user(username)
