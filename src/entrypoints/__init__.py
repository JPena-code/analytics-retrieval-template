from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_session, init_db

__all__ = ["init_app", "get_session"]


@asynccontextmanager
async def init_app(app: FastAPI):
    init_db()
    yield
