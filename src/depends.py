from typing import Annotated

from fastapi import Depends
from sqlmodel import Session as SqlSession

from .entrypoints import get_session

Session = Annotated[SqlSession, Depends(get_session)]
