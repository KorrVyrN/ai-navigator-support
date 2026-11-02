"""Offline retrieval from a supplied collection of knowledge articles."""
import re
from pydantic import BaseModel, Field

class Article(BaseModel):
    id: str
    title: str
    content: str = Field(min_length=1)

class SearchHit(BaseModel):
    id: str
    title: str
    excerpt: str
    score: int

def search_articles(query: str, articles: list[Article], limit: int = 3) -> list[SearchHit]:
    terms = set(re.findall(r"\w{3,}", query.casefold()))
    if not terms:
        return []
    hits = []
    for article in articles:
        title_terms = set(re.findall(r"\w{3,}", article.title.casefold()))
        body_terms = set(re.findall(r"\w{3,}", article.content.casefold()))
        score = len(terms & title_terms) * 3 + len(terms & body_terms)
        if score:
            hits.append(SearchHit(id=article.id, title=article.title,
                                  excerpt=article.content[:600], score=score))
    return sorted(hits, key=lambda hit: (-hit.score, hit.id))[:limit]
