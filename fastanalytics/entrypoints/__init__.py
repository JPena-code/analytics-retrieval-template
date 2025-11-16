from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_session, init_db
from .logger import get_logger, init_loggers

__all__ = ["init_app", "get_session"]


@asynccontextmanager
async def init_app(app: FastAPI):
    init_loggers()
    init_db(get_logger())
    yield {"logger": get_logger()}
