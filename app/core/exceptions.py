from fastapi import  FastAPI, Request, Exception
from fastapi.response import JSONResponse

def register_exception_nadlers(app:FastAPI):
    @app.add_exception_handler(Exception)
    async def unhandeled_exception_handler(request:Request, exc:Exception):
        return JSONResponse(status_code=500, content={'detail':str(exec)})