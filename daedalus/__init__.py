from daedalus.core.api.controller import Controller
from daedalus.core.api.controller_implementation import CImpl
from daedalus.core.api.decorator.search import search
from daedalus.core.api.decorator.mutate import mutate
from daedalus.core.api.decorator.delete import delete
from daedalus.core.api.decorator.get import get
from daedalus.core.bootstrap.bootstrapper import DaedalusBootstrapper

def initialize_daedalus():
    bootstrapper = DaedalusBootstrapper()
    app = bootstrapper.initialize()
    return app