from typing import Any, Dict, List

from daedalus.api.decorators.endpoint import endpoint
from daedalus.api.interface.response import Response
from daedalus.bootstrap.decorator.controller import Controller
from example.src.user.user_service import UserService


@Controller()
class UserController:
    inject = ['UserService']
    # Todo: refactor to remove this attribute
    api: Any
    # Todo: refactor to remove this attribute
    routes: List[Dict[str, Any]] = []

    def __init__(self, user_service: UserService):
        self.user_service = user_service
        # Todo: refactor to remove this call
        self.register_routes()

    # Todo: refactor to remove this method
    def register_routes(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_route'):
                route_info = attr._route
                self.routes.append(route_info)

    @endpoint(path="/user")
    def create_user_route(self, req):
        self.user_service.create_user("John Doe")
        return Response(
            status_code=200,
            data={"message": "User created"}
        )