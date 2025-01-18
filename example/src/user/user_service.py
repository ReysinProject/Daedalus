from daedalus.ioc.lazy_inject import LazyInject
from daedalus.ioc.service import Service


@Service()
class UserService:
    logger = LazyInject('LoggerService')

    def create_user(self, username):
        self.logger.log(f"User created: {username}")
