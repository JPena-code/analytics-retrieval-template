from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake

_config = ConfigDict(extra="allow", alias_generator=to_snake)


class HyperParams(BaseModel, extra="forbid"):
    """Parameter required by our API to create a hypertable"""

    model_config = _config

    table_name: str
    time_column: str
    time_interval: str | int
    if_not_exists: bool
    migrate_data: bool
    drop_after: str | int
    migrate_data: bool


class HyperTableSchema(BaseModel):
    """Base class for hypertables"""

    # Allow extra filed in case of new API interface changes
    # so it does not broke the application and can be fixed later
    model_config = _config

    hypertable_schema: str
    hypertable_name: str
    owner: str
    num_dimensions: int
    num_chunks: int
    compression_enabled: bool
    tablespaces: str | None = None
