from sqlalchemy.orm import declared_attr, declarative_base

from daedalus.database.mixin.id_mixin import IdMixin
from daedalus.database.mixin.soft_delete_mixin import SoftDeleteMixin
from daedalus.database.mixin.timestamp_mixin import TimestampMixin

SqlalchemyBase = declarative_base()

class DaedalusTable(SqlalchemyBase, IdMixin, TimestampMixin, SoftDeleteMixin):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()