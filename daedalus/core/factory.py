import inspect
import os

from daedalus.bootstrap.bootstrap_manager import BootstrapManager
from daedalus.bootstrap.module_node import ModuleNode
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

        Logger.info("Mapping modules...")
        self._entrypoint = ModuleNode(
            module=self._module,
            bootstrapper=self._bootstrap_manager
        )
        self._entrypoint.print()

    def serve(self, port:int=8080, host:str='localhost', cors: bool =False):
        """
        Serve Daedalus.
        :param cors:
        :param port:
        :param host:
        """
        is_secure = False
        Logger.info("Serving Daedalus on {}://{}:{}".format("https" if is_secure else "http",host, port))
