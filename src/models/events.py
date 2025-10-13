import uuid
from typing import Annotated

from pydantic import IPvAnyAddress, NonNegativeFloat, StringConstraints
from sqlalchemy.dialects.postgresql import INET
from sqlmodel import Field, String, Uuid

from .._types import Page
from .base import BaseHyperModel


class Event(BaseHyperModel, table=True):
    __tablename__ = "events"  # type: ignore

    page: Page
    agent: Annotated[str, StringConstraints(min_length=10)]
    ip_address: IPvAnyAddress = Field(sa_type=INET)
    referrer: str | None = Field(sa_type=String, nullable=True)
    session_id: uuid.UUID = Field(sa_type=Uuid)
    duration: NonNegativeFloat = 0
