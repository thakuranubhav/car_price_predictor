import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

# Configure logger level (INFO is silenced by default in Python's root logger)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)  # Fixed: pass 'request', not 'response'
        
        logger.info(f"Response: {response.status_code}")
        return response