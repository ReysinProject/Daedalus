from daedalus.bootstrap.decorator.service import Service


@Service()
class LoggerService:
    def log(self, message):
        print(f"Log: {message}")
