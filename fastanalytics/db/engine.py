from typing import TYPE_CHECKING

import sqlmodel

if TYPE_CHECKING:
    from typing import Any

    from sqlalchemy.engine import URL, Engine


def create_engine(url: "str | URL", timezone: str = "UTC", **kwargs: "Any") -> "Engine":
    conn_args = kwargs.get("connect_args", {})
    conn_args["options"] = f"-c timezone={timezone}"
    return sqlmodel.create_engine(
        url,
        connect_args=conn_args,
        execution_options={"isolation_level": "READ COMMITTED"},
        **kwargs,
    )
