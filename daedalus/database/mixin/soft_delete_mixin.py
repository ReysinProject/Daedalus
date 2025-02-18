from sqlalchemy import Column, DateTime, func


class SoftDeleteMixin(object):
    is_deleted = Column(DateTime, default=None)
    deleted_at = Column(DateTime, default=None)
    deleted_by = Column(DateTime, default=None)
