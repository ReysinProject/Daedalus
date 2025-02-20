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
        self.articles = [
            {
                'id': '1',
                'title': 'Hello World',
                'content': 'This is a test article',
                'author': 'John Doe'
            },
            {
                'id': '2',
                'title': 'Hello Universe',
                'content': 'This is another test article',
                'author': 'Jane Doe'
            }
        ]

    @get
    def get_article(self, id: int) -> ArticleModel:
        article = next((article for article in self.articles if article['id'] == id), None)
        if article:
            return article


    @post
    def create_article(self) -> str:
        return "Hello World"

    @delete
    def delete_article(self) -> str:
        return "Hello World"

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

