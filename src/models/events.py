import uuid
from typing import Annotated

from pydantic import AnyHttpUrl, IPvAnyAddress, NonNegativeFloat, StringConstraints
from sqlmodel import BigInteger, Field, String, Uuid

from .._types import Page
from .base import BaseHyperModel


class Event(BaseHyperModel, table=True):
    __tablename__ = "events"  # type: ignore

    req_id: uuid.UUID = Field(sa_type=Uuid, default_factory=uuid.uuid4)
    page: Page
    agent: Annotated[str, StringConstraints(min_length=10)]
    ip_address: Annotated[IPvAnyAddress, Field(sa_type=BigInteger)]
    # ip_address: str | None
    referrer: Annotated[AnyHttpUrl | None, Field(sa_type=String, nullable=True)]
    # referrer: str | None = None
    session_id: str | None
    duration: NonNegativeFloat = 0
