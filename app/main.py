"""Authenticated incident-analysis API."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.auth import require_api_token
from app.services.knowledge_search import Article, SearchHit, search_articles
from app.services.incident_detection import TicketInput, IncidentGroup, group_incidents
from app.config import get_settings
from app.services.gigachat_service import GigaChatError, GigaChatService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fail closed before accepting traffic if credentials are missing or invalid.
    try:
        settings = get_settings()
    except ValueError:
        raise RuntimeError('Invalid configuration; check required environment variables') from None
    service = GigaChatService(settings)
    app.state.gigachat = service
    try:
        yield
    finally:
        await service.close()


app = FastAPI(title='AI Navigator', version='0.2.0', lifespan=lifespan)


class IncidentRequest(BaseModel):
    description: str = Field(min_length=1, max_length=20000, pattern=r'\S')


class IncidentResponse(BaseModel):
    analysis: str
    requires_human_review: bool


@app.get('/')
def root():
    return {'name': 'AI Navigator', 'version': '0.2.0', 'status': 'running'}


@app.get('/health')
def health():
    return {'status': 'healthy'}


def get_service(request: Request) -> GigaChatService:
    return request.app.state.gigachat


@app.post('/api/v1/incidents/analyze', response_model=IncidentResponse,
          dependencies=[Depends(require_api_token)])
async def analyze_incident(body: IncidentRequest, service=Depends(get_service)):
    try:
        return await service.analyze_incident(body.description)
    except GigaChatError:
        raise HTTPException(502, 'GigaChat is unavailable; try again later') from None


class DetectRequest(BaseModel):
    tickets: list[TicketInput] = Field(min_length=1, max_length=1000)
    threshold: int = Field(default=3, ge=2, le=100)
    window_minutes: int = Field(default=60, ge=1, le=1440)


@app.post('/api/v1/incidents/detect', response_model=list[IncidentGroup],
          dependencies=[Depends(require_api_token)])
def detect_incidents(body: DetectRequest):
    """Offline grouping; no ticket data is sent to external services."""
    return group_incidents(body.tickets, body.threshold, body.window_minutes)


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    articles: list[Article] = Field(min_length=1, max_length=500)
    limit: int = Field(default=3, ge=1, le=10)


@app.post('/api/v1/knowledge/search', response_model=list[SearchHit],
          dependencies=[Depends(require_api_token)])
def knowledge_search(body: KnowledgeSearchRequest):
    return search_articles(body.query, body.articles, body.limit)
