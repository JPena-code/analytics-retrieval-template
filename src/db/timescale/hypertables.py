import logging

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from ...entrypoints.logger import LOGGER_NAME
from ...models import BaseTable
from .. import statements as sql
from .schemas import HyperTableSchema
from .utils import extract_model_hyper_params, hypertable_sql

LOGGER = logging.getLogger(LOGGER_NAME)


def sync_hypertables(conn: Connection):
    """Synchronize all tables associated with a model to be an hypertable in the database"""
    models = [
        model
        for model in BaseTable.__subclasses__()
        if getattr(model, "__table__", None) is not None
    ]
    LOGGER.debug("Found %d models to check for hypertables", len(models))
    current_tables = {table.hypertable_name for table in hypertables(conn)}
    models = [model for model in models if getattr(model, "__table__", None) not in current_tables]
    if not models:
        LOGGER.debug("No new models to create hypertables for")
        return
    LOGGER.info("Creating hypertables for models %s", models)
    for model in models:
        LOGGER.debug("Creating hypertable for model %s", model.__name__)
        try:
            create_hypertable(conn, model)
        except SQLAlchemyError as e_sql:
            LOGGER.error(
                "Could not create hypertable for model %s (%s) (%d) (%s)",
                model.__name__,
                type(e_sql).__name__,
                e_sql.code,
                e_sql._message(),
            )
            raise e_sql


def create_hypertable(conn: Connection, model: type[BaseTable]):
    """Create a hypertable for a given model, the associated table must exists in the database."""
    if model is None:
        raise ValueError("Model is required, cannot be None")
    if getattr(model, "__table__", None) is None:
        raise ValueError(f"Model {type(model).__name__} does not have been instantiated as a table")
    params = extract_model_hyper_params(model)
    statement = hypertable_sql(params)
    conn.execute(text(statement))


def hypertables(conn: Connection):
    """Fetch all the hypertables in the database"""
    tables = []
    try:
        tables = conn.execute(sql.AVAILABLE_HYPERTABLES).all()
        tables = [HyperTableSchema.model_validate(table._asdict()) for table in tables]
    except SQLAlchemyError as e_sql:
        LOGGER.fatal(
            "Could not fetch hypertables from database (%s) (%d) (%s)",
            type(e_sql).__name__,
            e_sql.code,
            e_sql._message(),
        )
        raise e_sql
    return tables
