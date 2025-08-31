from typing import TypedDict

from pydantic.alias_generators import to_snake

from ...models import BaseTable


class HyperParams(TypedDict):
    table_name: str
    time_column: bool
    time_interval: str
    drop_after: bool
    migrate_data: bool


def extract_model_hyper_params(model: type[BaseTable]):
    return HyperParams(
        **{
            "table_name": getattr(model, "__tablename__", to_snake(model.__name__)),
            "time_column": getattr(model, "__time_column__", None),
            "time_interval": getattr(model, "__time_interval__", None),
            "drop_after": getattr(model, "__drop_after__", None),
            "if_not_exists": True,
            "migrate_data": True,
        }
    )


def hyper_table_sql(params: HyperParams):
    pass
