import os
import sys
import importlib
import inspect
from typing import List, Type, Any, Optional

from daedalus.logger.logger import Logger

class BootstrapManager:
    def __init__(self, base_path: str):
        """
        Initialize the BootstrapManager.

        Args:
            base_path (str): The root directory path to scan for modules
        """
        self.base_path = os.path.abspath(base_path)
        # Add base_path to Python path if not already there
        if self.base_path not in sys.path:
            sys.path.insert(0, self.base_path)
        self.registered_classes: List[Type[Any]] = []

    def _is_target_file(self, filename: str) -> bool:
        """
        Check if the file matches the target patterns.

        Args:
            filename (str): Name of the file to check

        Returns:
            bool: True if the file matches any target pattern
        """
        patterns = ['.py']
        return any(filename.endswith(pattern) for pattern in patterns)

    def _get_module_name(self, file_path: str) -> str:
        """
        Convert file path to module import path.

        Args:
            file_path (str): Path to the Python file

        Returns:
            str: Module import path
        """
        relative_path = os.path.relpath(file_path, self.base_path)
        # Handle the case where the file is in the root directory
        if os.path.dirname(relative_path) == '':
            return os.path.splitext(relative_path)[0]

        # Convert path to module path
        module_path = relative_path.replace(os.path.sep, '.').replace('.py', '')
        return module_path

    def _has_target_decorator(self, cls: Type[Any]) -> bool:
        """
        Check if a class has either @Module() or @Service() decorator.

        Args:
            cls (Type[Any]): Class to check

        Returns:
            bool: True if class has target decorator
        """
        # Check if class has __decorated__ attribute which is typically
        # added by the decorators from daedalus.ioc
        if hasattr(cls, '__decorated__'):
            return True

        # Check if the class is a wrapper and has the __decorated__ attribute
        if hasattr(cls, '__wrapped__'):
            wrapped_cls = getattr(cls, '__wrapped__')
            if hasattr(wrapped_cls, '__decorated__'):
                return True

        return False

    def _scan_directory(self) -> List[str]:
        """
        Scan directory recursively for target files.

        Returns:
            List[str]: List of module paths to import
        """
        module_paths = []
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if self._is_target_file(file):
                    full_path = os.path.join(root, file)
                    module_path = self._get_module_name(full_path)
                    module_paths.append(module_path)
        return module_paths

    def register_all(self) -> List[Type[Any]]:
        """
        Register all decorated classes from target files.
        Only registers modules that contain exactly one decorated class.

        Returns:
            List[Type[Any]]: List of registered classes
        """
        module_paths = self._scan_directory()

        for module_path in module_paths:
            try:
                # Try to find parent package first if it exists
                parts = module_path.split('.')
                if len(parts) > 1:
                    parent_package = '.'.join(parts[:-1])
                    try:
                        importlib.import_module(parent_package)
                    except ImportError:
                        pass

                # Import the module
                module = importlib.import_module(module_path)

                # Get all classes defined in the module that have the target decorator
                decorated_classes = [
                    cls for name, cls in inspect.getmembers(module, inspect.isclass)
                    if (cls.__module__ == module_path and  # Only get classes defined in this module
                        self._has_target_decorator(cls))  # Only get decorated classes
                ]

                # Check if module contains exactly one decorated class
                if len(decorated_classes) == 0:
                    Logger.error(f"Error: Module {module_path} contains no valid decorated classes (@Module(), Controller() or @Service())")
                    continue
                elif len(decorated_classes) > 1:
                    Logger.error(f"Error: Module {module_path} contains multiple decorated classes. Each module should contain exactly one decorated class.")
                    Logger.error(f"Classes found: {[cls.__name__ for cls in decorated_classes]}")
                    continue

                # Add the single decorated class to registered classes
                self.registered_classes.append(decorated_classes[0])
                Logger.info(f"Registered class {decorated_classes[0].__name__} from module {module_path}")

            except ImportError as e:
                Logger.error(f"Error importing module {module_path}: {e}")
            except Exception as e:
                Logger.error(f"Error registering module {module_path}: {e}")

        return self.registered_classes

    def get_registered_classes(self) -> List[Type[Any]]:
        """
        Get all registered classes.

        Returns:
            List[Type[Any]]: List of registered classes
        """
        return self.registered_classes

    def get_class_by_name(self, class_name: str) -> Optional[Type[Any]]:
        """
        Get a registered class by its name.

        Args:
            class_name (str): Name of the class to find

        Returns:
            Optional[Type[Any]]: The requested class if found, None otherwise
        """
        for cls in self.registered_classes:
            if cls.__name__ == class_name:
                return cls
        return None
