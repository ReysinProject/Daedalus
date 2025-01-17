from daedalus.ioc.service import Service


@Service()
class LoggerService:
    def log(self, message):
        print(f"Log: {message}")
