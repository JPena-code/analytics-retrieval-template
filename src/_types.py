from typing import Annotated

from pydantic import StringConstraints

Page = Annotated[str, StringConstraints(pattern=r"^/.*$")]
