from daedalus import Controller, CImpl, get, post
from typing import List, Dict, Optional, Annotated
from pydantic import BaseModel

from daedalus.core.api.decorator.patch import patch
from daedalus.core.api.decorator.put import put
from daedalus.core.scheme.base import BaseScheme
from daedalus.crud.decorator.delete import delete


class ArticleModel(BaseScheme):
    id: int
    title: str
    content: str
    author: str

@Controller(
    prefix='/article',
    access_limitation=lambda ctx: True
)
class Article(CImpl):
    def __init__(self):
        super().__init__()
        self.articles: List[ArticleModel] = [
            ArticleModel(id=1, title="Hello World", content="Hello World", author="John Doe"),
            ArticleModel(id=2, title="Hello World", content="Hello World", author="John Doe"),
            ArticleModel(id=3, title="Hello World", content="Hello World", author="John Doe"),
        ]

    @get
    def get_article(self, id: int) -> ArticleModel:
        for article in self.articles:
            if article.id == id:
                return article


    # @post
    # def create_article(self, test: ArticleModel) -> str:
    #     return "Hello World"

    @delete
    def delete_article(self) -> ArticleModel:
        return ArticleModel(id=1, title="Hello World", content="Hello World", author="John Doe")

    @patch
    def update_article(self) -> str:
        return "Hello World"

    @put
    def put_article(self) -> str:
        return "Hello World"



    # @search
    # def search(self, author: Optional[str] = None) -> List[Dict]:
    #     """Search for articles, optionally filtered by author"""
    #     if author:
    #         return [article for article in self.articles if article['author'] == author]
    #     return self.articles
    #
    # @mutate
    # def mutate(self, title: str, content: str, author: str) -> Dict:
    #     """Create or update an article"""
    #     article = {
    #         'id': str(len(self.articles) + 1),
    #         'title': title,
    #         'content': content,
    #         'author': author
    #     }
    #     self.articles.append(article)
    #     return article
    #
    # @delete
    # def delete(self, id: str) -> Dict:
    #     """Delete an article by id"""
    #     for i, article in enumerate(self.articles):
    #         if article['id'] == id:
    #             deleted = self.articles.pop(i)
    #             return {"success": True, "deleted": deleted}
    #     return {"success": False, "message": "Article not found"}

