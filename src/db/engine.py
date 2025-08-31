import sqlalchemy
from sqlalchemy.engine import URL, Engine


def create_engine(url: str | URL, timezone="UTC", **kwargs) -> Engine:
    conn_args = kwargs.pop("connect_args", {})
    conn_args["options"] = f"-c timezone={timezone}"
    return sqlalchemy.create_engine(
        url,
        connect_args=conn_args,
        execution_options={"isolation_level": "READ COMMITTED"},
        **kwargs,
    )
