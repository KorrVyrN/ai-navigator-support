"""Authenticated incident-analysis API."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.auth import require_api_token
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
