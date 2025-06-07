import sqlalchemy.exc
from sqlalchemy import Engine


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

            trans.execute(sqlalchemy.text(f"CREATE EXTENSION IF NOT EXISTS {name} CASCADE"))
            trans.commit()
        except sqlalchemy.exc.SQLAlchemyError as e_sql:
            trans.rollback()
            raise e_sql
