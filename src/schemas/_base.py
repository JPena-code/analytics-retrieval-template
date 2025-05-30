from typing import TYPE_CHECKING, Generic, TypeVar

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal

if TYPE_CHECKING:
    from collections.abc import Iterable

_CONFIG_MODEL: ConfigDict = {
    "extra": "forbid",
    "alias_generator": AliasGenerator(serialization_alias=to_pascal),
}

T = TypeVar("T", "Base", "Iterable[Base]")


class Base(BaseModel):
    """Base model with configuration class"""

    model_config = _CONFIG_MODEL


class BaseCreateSchema(Base):
    """Base schema for creation operations."""

    pass


class Response(Base, Generic[T]):
    """Generic response model for API responses"""

    data: T
    metadata: dict
