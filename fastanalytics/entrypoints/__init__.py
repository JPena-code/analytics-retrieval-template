from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from .db import get_session, init_db
from .logger import get_logger, init_loggers

if TYPE_CHECKING:
    import logging
    from collections.abc import AsyncGenerator


__all__ = [
    "init_app",
    "get_session",
    "get_logger",
]


@asynccontextmanager
async def init_app(app: FastAPI) -> AsyncGenerator[dict[str, logging.Logger], None]:
    init_loggers()
    init_db(get_logger())
    yield {"logger": get_logger()}
