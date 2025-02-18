from daedalus.core.api.controller import Controller
from daedalus.core.api.controller_implementation import CImpl
from daedalus.core.api.decorator.search import search


@Controller(
    prefix='/article',
    access_limitation=lambda ctx: True
)
class Article(CImpl):

    @search
    def search(self):
        pass

    # @daedalus.mutate
    # def mutate(self, title: str, content: str):
    #     pass
    #
    # @daedalus.delete
    # def delete(self, id: str):
    #     pass
