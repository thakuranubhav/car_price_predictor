from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from fastapi.security import APIKeyHeader, HTTPBearer

from app.core.config import settings


api_key_scheme = APIKeyHeader(name="x-api-key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

def create_token(data:dict, expire_minutes=30):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=expire_minutes)
    to_encode.update({'exp':expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_token(token:str):
    try:
        payload=jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        return None
