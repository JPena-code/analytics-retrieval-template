from sqlmodel import Session

from ..db import activate_ext, create_engine, sync_hypertables
from ..settings import Settings

SETTINGS = Settings()  # type: ignore

__engine = None


def init_db():
    """Initialize the database connection and the related setup
    In a lifespan cycle for the application
    """

    __engine = create_engine(
        SETTINGS.pg_dsn.encoded_string(),
        echo=True,
        echo_pool=SETTINGS.debug,
        pool_size=10,
        pool_recycle=3600,
        pool_timeout=30,
    )
    activate_ext(__engine, "timescaledb")
    activate_ext(__engine, "uuid-ossp")
    sync_hypertables(__engine)


def get_session():
    """Get the a new session connected to the database"""
    if __engine is None:
        raise RuntimeError(
            "Database engine is not initialized yet... `init_db` must be called first "
            + "at the leve of lifespan of the application"
        )
    # TODO: should we use a sessionmaker here?
    with Session(__engine) as session:
        yield session
