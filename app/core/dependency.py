from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.security import api_key_scheme, bearer_scheme, verify_token


def get_api_key(api_key: str = Security(api_key_scheme)):
    if not api_key:
        raise HTTPException(status_code=403, detail="API key is missing")
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization token is missing")

    payload= verify_token(credentials.credentials)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Jwt token")

    return payload
