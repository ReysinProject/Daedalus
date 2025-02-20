import inspect
from inspect import Signature
from typing import Any, get_type_hints, Callable, Optional, Union, Type, get_args, get_origin
from collections.abc import Mapping, Sequence

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from daedalus.core.scheme.base import BaseScheme


class GraphQLGenerator:
    def __init__(self, app: FastAPI, controllers):
        self.app = app
        self.controllers = controllers
        self.graphql_queries = {}
        self.graphql_mutations = {}

    def _convert_type(self, scheme: Type, input: bool) -> Type:
        if issubclass(scheme, BaseScheme):
            print(f"Converting {scheme} to GraphQL")
            return scheme.to_graphql(as_input=input)
        print(f"Not converting {scheme} to GraphQL")
        return scheme

    def _create_resolver(self, method: Callable) -> strawberry.field:
        """Create a strawberry resolver from a controller method."""
        method_name = method.__name__
        signature: Signature = inspect.signature(method)

        # Convert return type
        return_type = self._convert_type(scheme=signature.return_annotation, input=False)

        def resolver_func(*args: Any, **kwargs: Any) -> Any:
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return method(*bound_args.args, **bound_args.kwargs)

        # Add proper signature and annotations
        resolver_func.__signature__ = signature
        resolver_func.__annotations__ = get_type_hints(method)

        # Process parameters for GraphQL
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            param_type = param.annotation if param.annotation is not inspect._empty else Any
            converted_type = self._convert_type(scheme=param_type, input=True)

            # Add type annotation to resolver
            resolver_func.__annotations__[param_name] = converted_type

        # Create the field with proper configuration
        field = strawberry.field(
            resolver=resolver_func,
            description=method.__doc__ or f"Resolver for {method_name}",
            graphql_type=return_type,
        )

        return field

    def generate(self):
        """Generate GraphQL schema using Strawberry."""
        for controller in self.controllers:
            for name, method in inspect.getmembers(controller, inspect.ismethod):
                if hasattr(method, '__decorated__'):
                    if hasattr(method, 'is_query'):
                        query_name = f"{name}"
                        self.graphql_queries[query_name] = self._create_resolver(method)
                        print(f"Registered GraphQL query: {query_name}")
                    elif hasattr(method, 'is_mutate'):
                        mutation_name = f"{name}"
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