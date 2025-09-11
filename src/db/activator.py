import logging

import sqlalchemy.exc
from sqlalchemy import Engine

from .._logger import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)


def activate_ext(engine: Engine, ext: str):
    """Activate an extension in the database.
    Args:
        engine (Engine): `sqlalchemy.Engine` instance connected to the database
        ext (str): The name of the extension to activate
    """
    with engine.begin() as trans:
        try:
            name = trans.execute(
                sqlalchemy.text(
                    "SELECT name FROM pg_available_extensions WHERE name = :ext"
                ).bindparams(ext=ext)
            ).scalar()
            if name is None:
                raise ValueError(f"Extension '{ext}' is not available in the database.")

            trans.execute(sqlalchemy.text(f'CREATE EXTENSION IF NOT EXISTS "{name}"'))
            trans.commit()
        except sqlalchemy.exc.SQLAlchemyError as e_sql:
            LOGGER.fatal(
                "Could not activate extension '%s' (%s) (%d) (%s)",
                ext,
                type(e_sql).__name__,
                e_sql.code,
                e_sql._message(),
            )
            trans.rollback()
            raise e_sql
        except ValueError:
            LOGGER.error("Extension (%s) is not available in server")
