from daedalus.bootstrap.decorator.service import Service
from example.src.logger.logger_service import LoggerService


@Service()
class UserService:
    inject = ['LoggerService']

    def __init__(self, logger_service: LoggerService):
        self.logger = logger_service

    def create_user(self, username):
        self.logger.log(f"User created: {username}")
