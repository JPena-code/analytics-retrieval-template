from typing import Annotated

from fastapi import Depends, Query
from sqlmodel import Session as SqlSession
from src.entrypoints import get_session
from src.schemas import Page

Session = Annotated[SqlSession, Depends(get_session)]

PageQuery = Annotated[Page, Query()]
