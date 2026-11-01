"""Validated server configuration. Secrets never appear in model representations."""
from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    navigator_api_token: SecretStr
    gigachat_api_key: SecretStr
    gigachat_scope: Literal['GIGACHAT_API_PERS', 'GIGACHAT_API_B2B', 'GIGACHAT_API_CORP'] = 'GIGACHAT_API_PERS'
    gigachat_model: str = 'GigaChat-2-Max'
    request_timeout_seconds: float = Field(default=30, gt=0, le=120)
    ca_bundle: str | None = None

    @field_validator('navigator_api_token', 'gigachat_api_key')
    @classmethod
    def validate_secret(cls, value: SecretStr, info):
        raw = value.get_secret_value()
        if not raw or raw.strip() != raw or any(c.isspace() for c in raw):
            raise ValueError('Secret must be nonempty and contain no whitespace')
        if raw.startswith(('your_', 'replace_', 'change_')):
            raise ValueError('Replace example secrets before starting')
        if info.field_name == 'navigator_api_token' and len(raw) < 32:
            raise ValueError('API token must contain at least 32 characters')
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
