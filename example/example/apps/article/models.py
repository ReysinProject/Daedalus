from sqlalchemy import Column, String, Text

from daedalus.database.base_model import DaedalusTable
from daedalus.database.decorator.model import model


@model
class Article(DaedalusTable):
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)