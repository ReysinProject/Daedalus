import inspect
import os

from daedalus.bootstrap.bootstrap_manager import BootstrapManager
from daedalus.logger.logger import Logger


class DaedalusFactory:

    @classmethod
    def create(cls, module):
        Logger.info("Creating Daedalus...")
        return cls(module)

    def __init__(self, module):
        self._module = module

        Logger.info("Registering modules...")
        self._bootstrap_manager = BootstrapManager(base_path=os.path.dirname(inspect.getfile(self._module)))
        self._bootstrap_manager.register_all()

        Logger.info("Mapping modules...")

    def serve(self):
        Logger.info("Serving Daedalus...")
