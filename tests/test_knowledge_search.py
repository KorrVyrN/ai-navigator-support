"""Knowledge retrieval unit tests."""
from app.services.knowledge_search import Article, search_articles

def test_search_returns_relevant_article():
    articles = [
        Article(id="pos", title="POS connectivity", content="Check the network connection"),
        Article(id="printer", title="Printer paper", content="Replace paper roll"),
    ]
    hits = search_articles("POS network", articles)
    assert len(hits) == 1
    assert hits[0].id == "pos"

def test_empty_query_returns_no_hits():
    assert search_articles("...", [Article(id="x", title="Test", content="Test content")]) == []

def test_search_is_limited():
    articles = [Article(id=str(i), title="POS", content="Network") for i in range(10)]
    assert len(search_articles("POS", articles, limit=2)) == 2
