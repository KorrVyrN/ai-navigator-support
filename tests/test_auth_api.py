import pytest
from fastapi.testclient import TestClient
from app.config import Settings, get_settings
from app.main import app, get_service
from app.services.gigachat_service import GigaChatError

TOKEN = 'a' * 43


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv('NAVIGATOR_API_TOKEN', TOKEN)
    monkeypatch.setenv('GIGACHAT_API_KEY', 'test-key')
    get_settings.cache_clear()
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    get_settings.cache_clear()


@pytest.mark.parametrize('header', [None, 'Bearer wrong', 'Basic abc', 'Bearer'])
def test_unauthenticated_request_rejected(client, header):
    headers = {'Authorization': header} if header else {}
    r = client.post('/api/v1/incidents/analyze', headers=headers, json={'description': 'test'})
    assert r.status_code == 401
    assert r.headers['www-authenticate'] == 'Bearer'


def test_public_health(client):
    assert client.get('/health').status_code == 200


@pytest.mark.parametrize('failure', [False, True])
def test_authorized_analysis(client, failure):
    class Service:
        async def analyze_incident(self, text):
            assert text == 'POS unavailable'
            if failure:
                raise GigaChatError('secret-provider-detail')
            return {'analysis': 'Check connectivity', 'requires_human_review': True}
    app.dependency_overrides[get_service] = lambda: Service()
    r = client.post('/api/v1/incidents/analyze', headers={'Authorization': f'Bearer {TOKEN}'},
                    json={'description': 'POS unavailable'})
    assert r.status_code == (502 if failure else 200)
    assert 'secret-provider-detail' not in r.text
    if not failure:
        assert r.json()['requires_human_review'] is True


@pytest.mark.parametrize('text', ['', '   ', 'x' * 20001], ids=['empty', 'whitespace', 'too-long'])
def test_input_validation(client, text):
    r = client.post('/api/v1/incidents/analyze', headers={'Authorization': f'Bearer {TOKEN}'},
                    json={'description': text})
    assert r.status_code == 422


def test_missing_settings_fail_closed(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv('NAVIGATOR_API_TOKEN', raising=False)
    monkeypatch.delenv('GIGACHAT_API_KEY', raising=False)
    get_settings.cache_clear()
    with pytest.raises(RuntimeError, match='Invalid configuration'):
        with TestClient(app):
            pass
    get_settings.cache_clear()


@pytest.mark.parametrize('token', ['short', 'replace_with_a_random_token_of_at_least_32_characters', 'x' * 32 + '\n'])
def test_bad_tokens_rejected(token):
    with pytest.raises(ValueError):
        Settings(_env_file=None, navigator_api_token=token, gigachat_api_key='key')


def test_secret_repr_redacted():
    settings = Settings(_env_file=None, navigator_api_token=TOKEN, gigachat_api_key='sensitive-key')
    assert TOKEN not in repr(settings)
    assert 'sensitive-key' not in repr(settings)
