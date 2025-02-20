from typing import Type, TypeVar, Optional, get_type_hints, ClassVar
from pydantic import BaseModel
import strawberry

T = TypeVar('T', bound='BaseScheme')


class BaseScheme(BaseModel):

    _graphql_type: ClassVar[Optional[Type]] = None

    @classmethod
    def to_rest(cls) -> Type[BaseModel]:
        """Return the REST version of the schema"""
        return cls

    @classmethod
    def to_graphql(cls) -> Type:
        """Return the GraphQL version of the schema"""
        if cls._graphql_type is None:
            fields = {}
            for name, field in cls.model_fields.items():
                field_type = field.annotation
                if field_type is None:
                    field_type = get_type_hints(cls)[name]
                fields[name] = strawberry.field(type_=field_type)

            cls._graphql_type = strawberry.type(
                type(
                    f"{cls.__name__}Type",
                    (),
                    fields
                )
            )
        return cls._graphql_type