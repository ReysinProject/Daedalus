from daedalus.api.decorators.endpoint import endpoint
from daedalus.api.interface.response import Response
from daedalus.bootstrap.decorator.controller import Controller
from example.src.count.count_service import CountService


@Controller()
class CountController:
    inject = ['CountService']

    def __init__(self, count_service: CountService):
        self.count_service = count_service

    @endpoint(path="/count")
    def count(self, req):
        count = self.count_service.add()
        return Response(
            status_code=200,
            data={"count": count}
        )