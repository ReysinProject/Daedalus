import inspect
from inspect import Signature
from typing import Any, get_type_hints, Callable

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

class GraphQLGenerator:
    def __init__(self, app, controllers):
        self.app = app
        self.controllers = controllers
        self.graphql_queries = {}
        self.graphql_mutations = {}

    def _create_resolver(self, method: Callable) -> strawberry.field:
        """Create a strawberry resolver from a controller method."""
        method_name = method.__name__
        signature = inspect.signature(method)
        return_type = signature.return_annotation

        if return_type is inspect._empty:
            return_type = str

        params = signature.parameters
        param_types = {name: param.annotation for name, param in params.items() if
                       param.annotation is not inspect._empty}

        def resolver_func(*args: Any, **kwargs: Any) -> return_type:
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return method(*bound_args.args, **bound_args.kwargs)

        resolver_func.__signature__ = signature
        resolver_func.__annotations__ = get_type_hints(method)

        resolver = strawberry.field(
            resolver=resolver_func,
            description=method.__doc__ or f"Resolver for {method_name}"
        )

        return resolver

    def generate(self):
        """Generate GraphQL schema using Strawberry."""
        for controller in self.controllers:
            prefix = getattr(controller, 'prefix', '')
            prefix_capitalized = ''.join(word.capitalize() for word in prefix.strip('/').split('_'))

            for name, method in inspect.getmembers(controller, inspect.ismethod):
                if hasattr(method, '__decorated__'):
                    if hasattr(method, 'is_query'):
                        query_name = f"{prefix_capitalized}"
                        self.graphql_queries[query_name] = self._create_resolver(method)
                        print(f"Registered GraphQL query: {query_name}")
                    elif hasattr(method, 'is_search'):
                        query_name = f"search{prefix_capitalized}"
                        self.graphql_queries[query_name] = self._create_resolver(method)
                        print(f"Registered GraphQL query: {query_name}")
                    elif hasattr(method, 'is_mutate') or hasattr(method, 'is_delete'):
                        operation = 'mutate' if hasattr(method, 'is_mutate') else 'delete'
                        mutation_name = f"{operation}{prefix_capitalized}"
                        self.graphql_mutations[mutation_name] = self._create_resolver(method)
                        print(f"Registered GraphQL mutation: {mutation_name}")

        if not self.graphql_queries:
            @strawberry.field
            def hello() -> str:
                return "Hello, world!"

            self.graphql_queries["hello"] = hello
            print("Added default 'hello' query")

        QueryType = type("Query", (), self.graphql_queries)
        query_type = strawberry.type(QueryType)

        mutation_type = None
        if self.graphql_mutations:
            MutationType = type("Mutation", (), self.graphql_mutations)
            mutation_type = strawberry.type(MutationType)

        schema = strawberry.Schema(query=query_type, mutation=mutation_type)
        graphql_app = GraphQLRouter(schema)
        self.app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])
        print("Registered GraphQL endpoint at /graphql")