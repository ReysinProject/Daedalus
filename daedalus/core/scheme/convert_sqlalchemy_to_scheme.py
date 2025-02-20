from daedalus.core.scheme.base import BaseScheme

def convert_sqlalchemy_to_scheme(
        model: Type[DeclarativeBase],
        base_scheme: Type[BaseScheme] = BaseScheme,
        exclude_fields: Set[str] = None,
        additional_fields: Dict[str, tuple[Type, Any]] = None,
        make_optional: Set[str] = None
) -> Type[BaseScheme]:
    """
    Convert a SQLAlchemy models to a daedalus scheme

    Args:
        model: SQLAlchemy model to convert
        base_scheme: Base scheme to inherit from
        exclude_fields: Exclude fields from the scheme
        additional_fields: Additional fields to add to the scheme
        make_optional: Fields to make optional

    Returns:
        The converted scheme
    """
    exclude_fields = exclude_fields or set()
    additional_fields = additional_fields or {}
    make_optional = make_optional or set()

    mapper = inspect(model)
    fields = {}

    for column in mapper.columns:
        if column.name in exclude_fields:
            continue

        python_type = column.type.python_type
        if column.name in make_optional:
            fields[column.name] = (Optional[python_type], None)
        else:
            fields[column.name] = (python_type, ...)

    fields.update(additional_fields)

    scheme_name = f"{model.__name__}Scheme"
    return create_model(
        scheme_name,
        __base__=base_scheme,
        **fields
    )