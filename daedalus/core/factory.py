import inspect
import os

from daedalus.bootstrap.bootstrap_manager import BootstrapManager
from daedalus.logger.logger import Logger


class DaedalusFactory:

    def __init__(self, module):
        """
        Initialize the Daedalus instance.
        Register and map modules.

        Args:
            module: The root module of the application

        Returns:
            Daedalus: The Daedalus instance
        """
        self._module = module

        Logger.info("Registering modules...")
        self._bootstrap_manager = BootstrapManager(base_path=os.path.dirname(inspect.getfile(self._module)))
        self._bootstrap_manager.register_all()
        print(self._bootstrap_manager.get_registered_classes())

        Logger.info("Mapping modules...")

    def serve(self):
        """
        Serve Daedalus.
        """
        Logger.info("Serving Daedalus...")
