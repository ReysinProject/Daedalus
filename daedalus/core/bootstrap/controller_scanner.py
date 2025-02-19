import inspect
import sys

class ControllerScanner:
    @staticmethod
    def scan():
        """Scan for controller classes and initialize them."""
        controllers = []
        for name, module in sys.modules.items():
            if name.startswith('daedalus') or name.startswith('example'):
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and getattr(obj, 'is_controller', False):
                        controller_instance = obj()
                        controllers.append(controller_instance)
        return controllers