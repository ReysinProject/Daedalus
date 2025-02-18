import uuid

from sqlalchemy import Column, String


class IdMixin(object):
    id: str = Column(String, primary_key=True, default=uuid.uuid4)