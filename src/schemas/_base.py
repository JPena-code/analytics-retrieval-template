from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal

_CONFIG_MODEL: ConfigDict = {"extra": "forbid", "alias_generator": to_pascal}


class Base(BaseModel):
    """Base model with configuration class"""

    model_config = _CONFIG_MODEL


class BaseCreateSchema(Base):
    """Base schema for creation operations."""

    pass
