from daedalus.bootstrap.decorator.service import Service


@Service()
class CountService:

    def __init__(self):
        self.count = 0

    def get(self):
        return self.count

    def add(self):
        self.count += 1
        return self.count
