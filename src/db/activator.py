import logging

import sqlalchemy.exc
from sqlalchemy import Connection

from .._logger import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)


def activate_ext(conn: Connection, ext: str):
    """Activate an extension in the database.
    Args:
        conn (Connection): `sqlalchemy.Connection` connection to the database
        ext (str): The name of the extension to activate
    """
    try:
        name = conn.execute(
            sqlalchemy.text(
                "SELECT name FROM pg_available_extensions WHERE name = :ext"
            ).bindparams(ext=ext)
        ).scalar()
        if name is None:
            raise ValueError(f"Extension '{ext}' is not available in the database.")

        conn.execute(sqlalchemy.text(f'CREATE EXTENSION IF NOT EXISTS "{name}"'))
    except sqlalchemy.exc.SQLAlchemyError as e_sql:
        LOGGER.fatal(
            "Could not activate extension '%s' (%s) (%d) (%s)",
            ext,
            type(e_sql).__name__,
            e_sql.code,
            e_sql._message(),
        )
        conn.rollback()
        raise e_sql
    except ValueError:
        LOGGER.error("Extension (%s) is not available in server")
