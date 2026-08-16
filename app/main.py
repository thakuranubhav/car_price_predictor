from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth, routes_predict
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import register_exception_nadlers
import dotenv

app= FastAPI(title='Car price prediction API')

# link middleware
app.add_middleware(LoggingMiddleware)

# link endpoint
app.include_router(routes_auth.router, tags=['Auth'])
app.include_router(routes_predict.router, tags=['Prediction'])

# Monitoring using prometheus
Instrumentator().instrument(app).expose(app)

#add exception hanlder
register_exception_nadlers(app)




