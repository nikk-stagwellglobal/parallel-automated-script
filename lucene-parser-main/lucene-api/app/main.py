from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import query_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="Lucene Query Parser API",
    description="Production-ready API for parsing Lucene queries with clean architecture",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_routes.router)

logger = get_logger(__name__)
