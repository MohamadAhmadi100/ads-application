import logging
from fastapi import Request, HTTPException
from app.main import app
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=422,
        content={"message": exc.detail},
    )
