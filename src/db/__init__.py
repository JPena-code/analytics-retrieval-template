# from sqlalchemy import text
# from sqlalchemy.orm import sessionmaker
# from sqlmodel import SQLModel, Session

from ..settings import Settings
from .activator import activate_ext
from .engine import create_engine
from .timescale.hypertables import sync_hypertables

__all__ = ["activate_ext", "init_db", "get_session"]


def init_db():
    """Initialize the database connection and the related setup
    In a lifespan cycle for the application
    """

    engine = create_engine(
        Settings.pg_dsn.encoded_string(),
        echo=True,
        echo_pool=True,
        pool_size=10,
        pool_recycle=3600,
        pool_timeout=30,
    )
    activate_ext(engine, "timescaledb")
    sync_hypertables(engine)


def get_session():
    pass
