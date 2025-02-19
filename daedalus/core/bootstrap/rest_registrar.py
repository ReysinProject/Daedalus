import inspect
from fastapi import APIRouter

class RESTRegistrar:
    def __init__(self, app, controllers):
        self.app = app
        self.controllers = controllers

    def register(self):
        """Register REST endpoints with FastAPI."""
        for controller in self.controllers:
            controller_router = APIRouter(
                prefix=getattr(controller, 'prefix', ''),
                tags=[controller.__class__.__name__]
            )

            for name, method in inspect.getmembers(controller, inspect.ismethod):
                if hasattr(method, '__decorated__'):
                    if hasattr(method, 'is_get'):
                        endpoint_path = f""
                        controller_router.get(endpoint_path)(method)
                        print(f"Registered REST GET endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_search'):
                        endpoint_path = f"/search"
                        controller_router.get(endpoint_path)(method)
                        print(f"Registered REST GET endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_mutate'):
                        endpoint_path = f"/mutate"
                        controller_router.post(endpoint_path)(method)
                        print(f"Registered REST POST endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_delete'):
                        endpoint_path = f"/delete"
                        controller_router.delete(endpoint_path)(method)
                        print(f"Registered REST DELETE endpoint: {endpoint_path}")
            self.app.include_router(controller_router)