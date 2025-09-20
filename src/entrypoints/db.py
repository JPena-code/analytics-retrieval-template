from sqlalchemy.schema import CreateSchema
from sqlmodel import SQLModel, Session

from .. import models
from ..db import activate_ext, create_engine, sync_hypertables
from ..settings import Settings

SETTINGS = Settings()  # type: ignore

__engine = create_engine(
    SETTINGS.pg_dsn.encoded_string(),
    echo=True,
    echo_pool=SETTINGS.debug,
    pool_size=100,
    pool_recycle=3600,
    pool_timeout=30,
)


def init_db():
    """Initialize the database connection and the related setup
    In a lifespan cycle for the application
    """
    if __engine is None:
        raise RuntimeError("Database engine is not initialized")
    with __engine.begin() as conn:
        try:
            conn.execute(CreateSchema(models.SCHEMA, if_not_exists=True))
            activate_ext(conn, "timescaledb")
            activate_ext(conn, "uuid-ossp")

            SQLModel.metadata.create_all(conn, checkfirst=True)
            sync_hypertables(conn)
        except:
            conn.rollback()
            raise


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
