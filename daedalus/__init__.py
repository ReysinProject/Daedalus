from daedalus.core.api.controller import Controller
from daedalus.core.api.controller_implementation import CImpl
from daedalus.crud.decorator.mutate import mutate
from daedalus.core.api.decorator.get import get
from daedalus.core.api.decorator.post import post
from daedalus.core.bootstrap.bootstrapper import DaedalusBootstrapper

def initialize_daedalus(graphql: bool = True, rest: bool = True):
    bootstrapper = DaedalusBootstrapper(
        graphql=graphql,
        rest=rest
    )
    app = bootstrapper.initialize()
    return app