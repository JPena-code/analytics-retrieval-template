from typing import Annotated

from pydantic import Field, IPvAnyAddress, NonNegativeFloat
from pydantic.types import StringConstraints

from ._base import BaseCreateSchema


class EventCreate(BaseCreateSchema):
    """Schema for the creation of a new event. i.e. POST /events"""

    path: Annotated[str, StringConstraints(pattern=r"^/.*$")]
    agent: Annotated[str, StringConstraints(min_length=10)]
    ip_address: IPvAnyAddress
    referrer: Annotated[str | None, Field(None)] = None
    session_id: str | None
    duration: NonNegativeFloat = 0
