from daedalus.database.decorator.model import model


@model
class Article(DaedalusTable):
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)