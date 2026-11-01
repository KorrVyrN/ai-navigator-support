import asyncio
import json
import time
from uuid import UUID
import httpx
import pytest
from app.config import Settings
from app.services.gigachat_service import GigaChatService, GigaChatError


def service(handler):
    settings = Settings(_env_file=None, navigator_api_token='a' * 43, gigachat_api_key='provider-secret')
    return GigaChatService(settings, transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
@pytest.mark.parametrize('scale', [1, 1000])
async def test_oauth_caching_and_masking(scale):
    counts = {'oauth': 0, 'chat': 0}
    def handler(request):
        if request.url.path.endswith('/oauth'):
            counts['oauth'] += 1
            assert request.headers['Authorization'] == 'Basic provider-secret'
            assert UUID(request.headers['RqUID']).version == 4
            assert request.content == b'scope=GIGACHAT_API_PERS'
            return httpx.Response(200, json={'access_token': 'access-secret', 'expires_at': (time.time() + 1800) * scale})
        counts['chat'] += 1
        assert request.headers['Authorization'] == 'Bearer access-secret'
        text = json.loads(request.content)['messages'][-1]['content']
        assert '495' not in text and 'person@example.com' not in text
        assert '[PHONE]' in text and '[EMAIL]' in text
        return httpx.Response(200, json={'choices': [{'message': {'content': 'Check provider'}}]})
    s = service(handler)
    try:
        for _ in range(2):
            await s.analyze_incident('+7 (495) 123-45-67 person@example.com')
        assert counts == {'oauth': 1, 'chat': 2}
        s._expires_at = time.time() - 1
        await s.analyze_incident('+7 (495) 123-45-67 person@example.com')
        assert counts['oauth'] == 2
    finally:
        await s.close()
    assert s._token is None


@pytest.mark.asyncio
@pytest.mark.parametrize('persistent', [False, True])
async def test_401_refresh_bounded(persistent):
    counts = {'oauth': 0, 'chat': 0}
    def handler(request):
        if request.url.path.endswith('/oauth'):
            counts['oauth'] += 1
            return httpx.Response(200, json={'access_token': str(counts['oauth']), 'expires_at': time.time() + 1800})
        counts['chat'] += 1
        if persistent or counts['chat'] == 1:
            return httpx.Response(401, text='secret')
        return httpx.Response(200, json={'choices': [{'message': {'content': 'OK'}}]})
    s = service(handler)
    try:
        if persistent:
            with pytest.raises(GigaChatError):
                await s.analyze_incident('test')
        else:
            assert (await s.analyze_incident('test'))['analysis'] == 'OK'
        assert counts == {'oauth': 2, 'chat': 2}
    finally:
        await s.close()


@pytest.mark.asyncio
async def test_concurrent_requests_share_token():
    oauth = []
    def handler(request):
        if request.url.path.endswith('/oauth'):
            oauth.append(request)
            return httpx.Response(200, json={'access_token': 'access', 'expires_at': time.time() + 1800})
        return httpx.Response(200, json={'choices': [{'message': {'content': 'OK'}}]})
    s = service(handler)
    try:
        await asyncio.gather(*(s.analyze_incident('test') for _ in range(5)))
        assert len(oauth) == 1
    finally:
        await s.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('mode', ['oauth401', 'timeout', 'malformed', 'expired', 'chat500', 'chat_malformed'])
async def test_failures_do_not_leak_credentials(mode):
    def handler(request):
        oauth = request.url.path.endswith('/oauth')
        if mode == 'timeout':
            raise httpx.ReadTimeout('provider-secret', request=request)
        if oauth:
            if mode == 'oauth401':
                return httpx.Response(401, text='provider-secret')
            if mode == 'malformed':
                return httpx.Response(200, json={})
            return httpx.Response(200, json={'access_token': 'access-secret', 'expires_at': time.time() + (-1 if mode == 'expired' else 1800)})
        if mode == 'chat500':
            return httpx.Response(500, text='provider-secret')
        return httpx.Response(200, json={'choices': []})
    s = service(handler)
    try:
        with pytest.raises(GigaChatError) as error:
            await s.analyze_incident('test')
        assert 'secret' not in str(error.value)
    finally:
        await s.close()
