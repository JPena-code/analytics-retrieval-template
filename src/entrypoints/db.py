from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateSchema
from sqlmodel import SQLModel, Session

from .. import models
from ..db import activate_ext, create_engine, sync_hypertables
from ..settings import Settings

__engine = create_engine(
    Settings.pg_dsn.encoded_string(),
    echo=True,
    echo_pool=Settings.debug,
    pool_size=100,
    pool_recycle=3600,
    pool_timeout=30,
)


def init_db(logger):
    """Initialize the database connection and the related setup
    In a lifespan cycle for the application
    """
    if __engine is None:
        raise RuntimeError("Database engine is not initialized")
    with __engine.begin() as conn:
        try:
            logger.info("Creating base schema %s", models.SCHEMA)
            conn.execute(CreateSchema(models.SCHEMA, if_not_exists=True))
            logger.debug('Creating extensions in database ["timescaledb", "uuid-ossp"')
            activate_ext(conn, "timescaledb")
            activate_ext(conn, "uuid-ossp")

            logger.info("Creating/Updating table models")
            SQLModel.metadata.create_all(conn, checkfirst=True)
            sync_hypertables(logger, conn)
        except SQLAlchemyError as e_sql:
            logger.error(
                "SQL Error encounter init_db (%s) (%d) (%s)",
                type(e_sql).__name__,
                e_sql.code,
                e_sql._message(),
            )
            conn.rollback()
            raise e_sql
        except:
            logger.exception("Unexpected error encounter init_db")
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
