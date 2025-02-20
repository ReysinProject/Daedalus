from fastapi import APIRouter, FastAPI
from daedalus.core.bootstrap.controller_scanner import ControllerScanner
from daedalus.core.bootstrap.graphql_generator import GraphQLGenerator
from daedalus.core.bootstrap.rest_registrar import RESTRegistrar


class DaedalusBootstrapper:
    def __init__(
            self,
            graphql: bool = True,
            rest: bool = True
    ):
        self.app = FastAPI()
        self.controllers = []
        self.router = APIRouter()
        self.graphql_queries = {}
        self.graphql_mutations = {}

        self.graphql = graphql
        self.rest = rest

    def initialize(self):
        """Initialize the Daedalus framework with FastAPI and Strawberry."""
        print("Scanning for controllers...")
        self.controllers = ControllerScanner.scan()
        print(f"Found {len(self.controllers)} controllers")

        if self.graphql:
            print("Generating GraphQL schema...")
            GraphQLGenerator(self.app, self.controllers).generate()

        if self.rest:
            print("Registering REST endpoints...")
            RESTRegistrar(self.app, self.controllers).register()

        return self.app