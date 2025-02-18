from functools import wraps
from typing import Callable, Any, TypeVar
import inspect
import strawberry
import uvicorn
from fastapi import APIRouter, Depends, FastAPI

T = TypeVar('T')


def search(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    # Store metadata for the bootstrapper
    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_search', True)
    setattr(wrapper, 'original_func', func)

    # Store the signature for schema generation
    signature = inspect.signature(func)
    setattr(wrapper, 'signature', signature)

    return wrapper


def mutate(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_mutate', True)
    setattr(wrapper, 'original_func', func)

    signature = inspect.signature(func)
    setattr(wrapper, 'signature', signature)

    return wrapper


def delete(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    setattr(wrapper, '__decorated__', True)
    setattr(wrapper, 'is_delete', True)
    setattr(wrapper, 'original_func', func)

    signature = inspect.signature(func)
    setattr(wrapper, 'signature', signature)

    return wrapper


class DaedalusBootstrapper:
    def __init__(self):
        self.app = FastAPI()
        self.controllers = []
        self.router = APIRouter()
        self.graphql_queries = {}
        self.graphql_mutations = {}

    def scan_controllers(self):
        """Scan for controller classes and initialize them."""
        import sys
        for name, module in sys.modules.items():
            if name.startswith('daedalus'):
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and getattr(obj, 'is_controller', False):
                        controller_instance = obj()
                        self.controllers.append(controller_instance)

    def register_rest_endpoints(self):
        """Register REST endpoints with FastAPI."""
        for controller in self.controllers:
            prefix = getattr(controller, 'prefix', '')

            for name, method in inspect.getmembers(controller, inspect.ismethod):
                if hasattr(method, '__decorated__'):
                    # Register endpoints based on decorator type
                    if hasattr(method, 'is_search'):
                        self.router.get(f"{prefix}/search")(method)
                    elif hasattr(method, 'is_mutate'):
                        self.router.post(f"{prefix}/mutate")(method)
                    elif hasattr(method, 'is_delete'):
                        self.router.delete(f"{prefix}/delete")(method)

        # Add router to the FastAPI app
        self.app.include_router(self.router)

    def generate_graphql_schema(self):
        """Generate GraphQL schema using Strawberry."""
        for controller in self.controllers:
            prefix = getattr(controller, 'prefix', '')
            prefix_capitalized = ''.join(word.capitalize() for word in prefix.strip('/').split('_'))

            for name, method in inspect.getmembers(controller, inspect.ismethod):
                if hasattr(method, '__decorated__'):
                    if hasattr(method, 'is_search'):
                        query_name = f"search{prefix_capitalized}"
                        self.graphql_queries[query_name] = self._create_resolver(method)
                    elif hasattr(method, 'is_mutate') or hasattr(method, 'is_delete'):
                        mutation_name = f"{'mutate' if hasattr(method, 'is_mutate') else 'delete'}{prefix_capitalized}"
                        self.graphql_mutations[mutation_name] = self._create_resolver(method)

        # Dynamically create query and mutation types
        query_fields = {name: field for name, field in self.graphql_queries.items()}
        mutation_fields = {name: field for name, field in self.graphql_mutations.items()}

        @strawberry.type
        class Query:
            pass

        @strawberry.type
        class Mutation:
            pass

        # Dynamically add fields to Query and Mutation classes
        for name, resolver in self.graphql_queries.items():
            setattr(Query, name, resolver)

        for name, resolver in self.graphql_mutations.items():
            setattr(Mutation, name, resolver)

        # Create schema
        schema = strawberry.Schema(query=Query, mutation=Mutation if mutation_fields else None)

        # Add GraphQL endpoint to FastAPI
        from strawberry.fastapi import GraphQLRouter
        graphql_app = GraphQLRouter(schema)
        self.app.include_router(graphql_app, prefix="/graphql")

    def _create_resolver(self, method):
        """Create a strawberry resolver from a controller method."""
        signature = getattr(method, 'signature')

        # Convert Python types to Strawberry types (simplified)
        type_mapping = {
            str: strawberry.scalar(str),
            int: strawberry.scalar(int),
            float: strawberry.scalar(float),
            bool: strawberry.scalar(bool),
            list: strawberry.list,
        }

        # Extract parameters for strawberry field
        params = {}
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            param_type = param.annotation
            if param_type in type_mapping:
                params[param_name] = type_mapping[param_type]
            else:
                params[param_name] = strawberry.scalar(Any)

        # Create resolver function
        @strawberry.field
        def resolver(**kwargs):
            return method(**kwargs)

        return resolver

    def initialize(self):
        """Initialize the Daedalus framework with FastAPI and Strawberry."""
        self.scan_controllers()
        self.register_rest_endpoints()
        self.generate_graphql_schema()
        return self.app


# Usage example:
def initialize_daedalus():
    bootstrapper = DaedalusBootstrapper()
    app = bootstrapper.initialize()
    return app

app = initialize_daedalus()

uvicorn.run(app, host="0.0.0.0", port=8000)