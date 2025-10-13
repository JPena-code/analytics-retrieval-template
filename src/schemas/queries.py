from typing import Annotated

from pydantic import ConfigDict, Field, PositiveInt
from pydantic.alias_generators import to_camel, to_snake

from ._base import Base

PageLimit = Annotated[PositiveInt, Field(ge=1, le=1000)]
PageOffset = Annotated[PositiveInt, Field(default=1)]


class Page(Base):
    model_config = ConfigDict(
        alias_generator=to_snake,
        title="Pagination Query",
        extra="ignore",
        validate_by_name=True,
    )

    page_size: PageLimit = 500
    page: PageOffset = 1


class PageMetaData(Page):
    model_config = ConfigDict(
        title="Pagination Meta Data",
        alias_generator=to_camel,
        extra="forbid",
    )

    total_records: PositiveInt
    total_pages: PositiveInt
