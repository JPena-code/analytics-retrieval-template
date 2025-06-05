from collections.abc import Sequence
from typing import Generic, TypeVar

from fastapi import Request
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

_CONFIG_MODEL: ConfigDict = {
    "extra": "forbid",
    "alias_generator": AliasGenerator(serialization_alias=to_camel),
}

T = TypeVar("T", bound="Base")


class Base(BaseModel):
    """Base model with configuration class"""

    model_config = _CONFIG_MODEL


class BaseCreateSchema(Base):
    """Base schema for creation operations."""

    pass


class Response(Base, Generic[T], arbitrary_types_allowed=True):
    """Generic response model for API responses"""

    data: T | Sequence[T] = Field(union_mode="smart")
    meta: dict = Field(default={}, init=False)
    req: Request = Field(
        exclude=True,
    )

    @model_validator(mode="after")
    def validate_meta(self):
        self.meta = {
            "total": len(self.data) if isinstance(self.data, Sequence) else 1,
            "offset": self.req.query_params.get("offset", 0),
            "limit": self.req.query_params.get("limit", 100),
            "status": "success",
            "message": "Request processed successfully",
        }
        return self
