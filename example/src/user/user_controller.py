from daedalus.api.decorators.endpoint import endpoint
from daedalus.api.interface.response import Response
from daedalus.bootstrap.decorator.controller import Controller
from example.src.user.user_service import UserService


@Controller()
class UserController:
    inject = ['UserService']

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @endpoint(path="/user")
    def create_user_route(self):
        self.user_service.create_user("John Doe")
        return Response(
            status_code=200,
            data={"message": "User created"}
        )