from daedalus import Controller, CImpl, search, mutate, delete, get
from typing import List, Dict, Optional, Annotated
from pydantic import BaseModel


class ArticleModel(BaseModel):
    id: Optional[str] = None
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
        self.articles = []  # In-memory store for this example

    @get
    def example_query(self, name: str) -> str:
        print(name)
        return "Hello " + name + "!"

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

