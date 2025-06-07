from datetime import datetime
from typing import Annotated

from pydantic import AnyHttpUrl, IPvAnyAddress, NonNegativeFloat, StringConstraints
from sqlmodel import TIMESTAMP, Field, SQLModel

from .._types import Page
from ..utils import get_utc_now


class Event(SQLModel, table=True):
    id: int = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
        nullable=False,
    )
    time: datetime = Field(
        default_factory=get_utc_now,
        nullable=False,
        sa_type=TIMESTAMP,
        primary_key=True,
    )
    page: Page
    agent: Annotated[str, StringConstraints(min_length=10)]
    ip_address: IPvAnyAddress
    referrer: Annotated[AnyHttpUrl | None, Field(None)] = None
    session_id: str | None
    duration: NonNegativeFloat = 0
