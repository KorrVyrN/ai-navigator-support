"""Server-to-server bearer authentication; no user accounts or JWT issuance."""
import hashlib
import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings

bearer = HTTPBearer(auto_error=False)


def require_api_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    settings: Settings = Depends(get_settings),
) -> None:
    supplied = credentials.credentials if credentials else ''
    expected = settings.navigator_api_token.get_secret_value()
    # Fixed-size digests also support arbitrary Unicode input without a 500 error.
    valid = secrets.compare_digest(
        hashlib.sha256(supplied.encode()).digest(),
        hashlib.sha256(expected.encode()).digest(),
    )
    if not credentials or credentials.scheme.lower() != 'bearer' or not valid:
        raise HTTPException(
            status_code=401, detail='Invalid or missing API token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
