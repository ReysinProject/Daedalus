from typing import Type, TypeVar, Optional, get_type_hints, ClassVar, Any, Union
from pydantic import BaseModel
import strawberry
from enum import Enum

T = TypeVar('T', bound='BaseScheme')

def convert_type(python_type: Type) -> Type:
    """Convert Python/Pydantic types to Strawberry-compatible types."""
    # Handle Optional types
    if hasattr(python_type, "__origin__") and python_type.__origin__ is Union:
        args = python_type.__args__
        if len(args) == 2 and isinstance(None, args[1]):
            return Optional[convert_type(args[0])]

    # Handle lists
    if hasattr(python_type, "__origin__") and python_type.__origin__ is list:
        return list[convert_type(python_type.__args__[0])]

    # Handle enums
    if isinstance(python_type, type) and issubclass(python_type, Enum):
        return strawberry.enum(python_type)

    # Handle BaseScheme types
    if isinstance(python_type, type) and issubclass(python_type, BaseScheme):
        return python_type.to_graphql()

    # Map basic Python types to Strawberry types
    type_mapping = {
        str: str,
        int: int,
        float: float,
        bool: bool,
        dict: Any,  # You might want to handle this differently
    }

    return type_mapping.get(python_type, python_type)

class BaseScheme(BaseModel):
    _graphql_type: ClassVar[Optional[Type]] = None
    _graphql_input_type: ClassVar[Optional[Type]] = None

    @classmethod
    def to_rest(cls) -> Type[BaseModel]:
        """Return the REST version of the schema"""
        return cls

    @classmethod
    def to_graphql(cls, as_input: bool = False) -> Type:
        """
        Return the GraphQL version of the schema

        Args:
            as_input: If True, returns an input type for mutations/arguments
                     If False, returns an output type for queries/returns
        """
        if as_input:
            if cls._graphql_input_type is None:
                fields = {}
                for name, field in cls.model_fields.items():
                    field_type = field.annotation
                    if field_type is None:
                        field_type = get_type_hints(cls)[name]

                    converted_type = convert_type(field_type)
                    default_value = field.default if field.default is not None else strawberry.UNSET
                    fields[name] = (converted_type, default_value)

                print(f"Creating input type for {cls.__name__}")
                print(fields)

                # Dynamically create a class with the fields as class attributes
                input_cls = type(
                    f"{cls.__name__}Input",
                    (),
                    {name: converted_type for name, (converted_type, default) in fields.items()}
                )

                # Set default values for fields
                for name, (_, default) in fields.items():
                    setattr(input_cls, name, default)

                cls._graphql_input_type = strawberry.input(input_cls)
            return cls._graphql_input_type
        else:
            if cls._graphql_type is None:
                fields = {}
                for name, field in cls.model_fields.items():
                    field_type = field.annotation
                    if field_type is None:
                        field_type = get_type_hints(cls)[name]

                    converted_type = convert_type(field_type)
                    fields[name] = strawberry.field(graphql_type=converted_type)

                cls._graphql_type = strawberry.type(
                    type(
                        f"{cls.__name__}Type",
                        (),
                        fields
                    )
                )
            return cls._graphql_type
