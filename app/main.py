import uvicorn
import logging
from fastapi import FastAPI
from app.config import settings
from app.user.router import router as user_router
from app.ad.router import router as ad_router
from app.comment.router import router as comment_router
from app.helpers.log_handler import LogHandler

app = FastAPI(
    title="AD Application",
    description="This is a tiny AD application!",
    version="0.0.1",
    docs_url="/docs/" if settings.DEBUG_MODE else None,
    redoc_url="/redoc/" if settings.DEBUG_MODE else None,
)

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(ad_router, prefix="/ad", tags=["ad"])
app.include_router(comment_router, prefix="/comment", tags=["comment"])


@app.on_event("startup")
async def startup_event() -> None:
    """
    This function will be called when the application starts.
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        filename="app.log",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Application is starting...")


@app.on_event("shutdown")
def shutdown_event() -> None:
    """
    This function will be called when the application stops.
    """
    logging.info("Application is shutting down...")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        LogHandler("logs/app.log", mode="a", maxBytes=5_000_000, backupCount=8),
    ],
)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=True,
    )
