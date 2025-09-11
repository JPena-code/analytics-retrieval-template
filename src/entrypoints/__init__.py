from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import init_db

__all__ = ["init_app"]


@asynccontextmanager
async def init_app(app: FastAPI):
    init_db()
    yield
