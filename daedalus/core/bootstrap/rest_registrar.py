import inspect
from typing import List

from fastapi import APIRouter, FastAPI


class RESTRegistrar:
    def __init__(self, app: FastAPI, controllers: List):
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
                        endpoint_path = f"/{name}"
                        controller_router.get(endpoint_path)(method)
                        print(f"Registered REST GET endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_delete'):
                        endpoint_path = f"/{name}"
                        controller_router.delete(endpoint_path)(method)
                        print(f"Registered REST DELETE endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_put'):
                        endpoint_path = f"/{name}"
                        controller_router.put(endpoint_path)(method)
                        print(f"Registered REST PUT endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_patch'):
                        endpoint_path = f"/{name}"
                        controller_router.patch(endpoint_path)(method)
                        print(f"Registered REST PATCH endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_post'):
                        endpoint_path = f"/{name}"
                        controller_router.post(endpoint_path)(method)
                        print(f"Registered REST POST endpoint: {endpoint_path}")

            self.app.include_router(controller_router)