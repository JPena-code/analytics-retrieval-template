from datetime import datetime
from typing import Annotated

from pydantic import AnyHttpUrl, Field, IPvAnyAddress, NonNegativeFloat
from pydantic.types import StringConstraints

from .._types import Page
from ..utils import get_utc_now
from ._base import Base


class EventCreate(Base):
    """Schema for the creation of a new event. i.e. POST /events"""

    path: Page
    agent: Annotated[str, StringConstraints(min_length=10)]
    ip_address: IPvAnyAddress
    referrer: Annotated[AnyHttpUrl | None, Field(None)] = None
    session_id: str | None
    duration: NonNegativeFloat = 0


class Event(EventCreate):
    """Schema for the event model. i.e. GET /events/{id}"""

    id: int
    time: datetime = Field(default_factory=get_utc_now)
