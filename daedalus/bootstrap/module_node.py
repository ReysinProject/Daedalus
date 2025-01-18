from daedalus.bootstrap.bootstrap_manager import BootstrapManager


class ModuleNode:

    def __init__(self, module, bootstrapper: BootstrapManager):
        """
        Initialize the ModuleNode instance.

        Args:
            module: The module
            bootstrapper: The BootstrapManager instance
        """
        self.name = module.__name__
        self._module = module()
        self._bootstrapper = bootstrapper
        self._imports = []
        self._providers = []

        self._get_providers()
        self._get_imports()
        self._get_controllers()

    def _get_providers(self):
        """
        Get providers from the module.

        Returns:
            list: The providers
        """
        for provider in self._module.providers:
            self._providers.append(
                self._inject_and_init(injectable=self._bootstrapper.get_class_by_name(provider))
            )

    def _get_controllers(self):
        """
        Get controllers from the module.

        Returns:
            list: The controllers
        """
        for controller in self._module.controllers:
            controller = self._bootstrapper.get_class_by_name(controller)

            self._providers.append(
                self._inject_and_init(injectable=controller)
            )

    def _get_imports(self):
        """
        Get imports from the module.

        Returns:
            list: The imports
        """
        imports = self._module.imports

        for import_module in imports:
            self._imports.append(
                ModuleNode(
                    module=self._bootstrapper.get_class_by_name(import_module),
                    bootstrapper=self._bootstrapper
                )
            )

    def _inject_and_init(self, injectable):
        """
        Inject dependencies and initialize the object.

        Args:
            injectable: The object to inject dependencies into
        """
        if hasattr(injectable, 'inject'):
            dependencies = [self._bootstrapper.get_class_by_name(dep if isinstance(dep, str) else dep.__name__) for dep in injectable.inject]
            return injectable(*dependencies)
        else:
            return injectable()

    def print(self, level=0):
        """
        Print the module node in a simplified format.

        Args:
            level: The indentation level
        """
        indent = "    " * level  # indentation based on the level

        # Print module name
        print(f"{indent}{self.name}")

        # Print providers and controllers
        providers = [p.__name__ if hasattr(p, '__name__') else str(p) for p in self._providers]
        controllers = [c.__name__ if hasattr(c, '__name__') else str(c) for c in self._module.controllers]

        print(f"{indent}  Providers: [{', '.join(f"{p}" for p in providers)}]")
        print(f"{indent}  Controllers: [{', '.join(f"{c}" for c in controllers)}]")

        # Print imports
        if self._imports:
            print(f"{indent}  Imports:")
            for i, import_node in enumerate(self._imports):
                import_node.print(level + 1)

