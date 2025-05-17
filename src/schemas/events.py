from pydantic import AnyHttpUrl, Field, IPvAnyAddress, NonNegativeInt

from ._base import BaseCreateSchema


class EventCreate(BaseCreateSchema):
    """Schema for the creation of a new event. i.e. POST /events"""

    path: AnyHttpUrl
    agent: str = Field("")
    ip_address: IPvAnyAddress
    referrer: str | None = Field(None)
    session_id: str | None
    duration: NonNegativeInt = Field(0, validate_default=False)
