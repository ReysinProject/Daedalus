import inspect
import sys
from typing import List, Dict, Any, Optional
import strawberry
from fastapi import APIRouter, FastAPI
from strawberry.fastapi import GraphQLRouter


class DaedalusBootstrapper:
    def __init__(self):
        self.app = FastAPI()
        self.controllers = []
        self.router = APIRouter()
        self.graphql_queries = {}
        self.graphql_mutations = {}

    def scan_controllers(self):
        """Scan for controller classes and initialize them."""
        for name, module in sys.modules.items():
            if name.startswith('daedalus') or name.startswith('example'):
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
                        endpoint_path = f"{prefix}/search"
                        self.router.get(endpoint_path)(method)
                        print(f"Registered REST GET endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_mutate'):
                        endpoint_path = f"{prefix}/mutate"
                        self.router.post(endpoint_path)(method)
                        print(f"Registered REST POST endpoint: {endpoint_path}")
                    elif hasattr(method, 'is_delete'):
                        endpoint_path = f"{prefix}/delete"
                        self.router.delete(endpoint_path)(method)
                        print(f"Registered REST DELETE endpoint: {endpoint_path}")

        # Add router to the FastAPI app
        self.app.include_router(self.router)

    def _create_resolver(self, method):
        """Create a strawberry resolver from a controller method."""
        method_name = method.__name__
        signature = getattr(method, 'signature')
        return_type = signature.return_annotation

        # Handle case where return_type is None or inspect._empty
        if return_type is inspect._empty:
            return_type = str

        # Create resolver function
        def resolver_func(*args, **kwargs):
            return method(*args, **kwargs)

        # Decorate with strawberry.field
        resolver = strawberry.field(
            resolver=resolver_func,
            description=method.__doc__ or f"Resolver for {method_name}"
        )

        return resolver

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
                        print(f"Registered GraphQL query: {query_name}")
                    elif hasattr(method, 'is_mutate') or hasattr(method, 'is_delete'):
                        operation = 'mutate' if hasattr(method, 'is_mutate') else 'delete'
                        mutation_name = f"{operation}{prefix_capitalized}"
                        self.graphql_mutations[mutation_name] = self._create_resolver(method)
                        print(f"Registered GraphQL mutation: {mutation_name}")

        # Add a default query if none are found
        if not self.graphql_queries:
            @strawberry.field
            def hello() -> str:
                return "Hello, world!"

            self.graphql_queries["hello"] = hello
            print("Added default 'hello' query")

        # Create Query type with the fields
        QueryType = type("Query", (), self.graphql_queries)
        query_type = strawberry.type(QueryType)

        # Create Mutation type if there are mutations
        mutation_type = None
        if self.graphql_mutations:
            MutationType = type("Mutation", (), self.graphql_mutations)
            mutation_type = strawberry.type(MutationType)

        # Create schema
        schema = strawberry.Schema(query=query_type, mutation=mutation_type)

        # Add GraphQL endpoint to FastAPI
        graphql_app = GraphQLRouter(schema)
        self.app.include_router(graphql_app, prefix="/graphql")
        print("Registered GraphQL endpoint at /graphql")

    def initialize(self):
        """Initialize the Daedalus framework with FastAPI and Strawberry."""
        print("Scanning for controllers...")
        self.scan_controllers()
        print(f"Found {len(self.controllers)} controllers")

        print("Registering REST endpoints...")
        self.register_rest_endpoints()

        print("Generating GraphQL schema...")
        self.generate_graphql_schema()

        return self.app