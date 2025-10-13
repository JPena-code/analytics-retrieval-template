from ipaddress import IPv4Address

from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from config import constants
from depends import PageQuery, Session
from schemas import EventCreate, EventSchema, Page, Response, ResponsePage, StatusEnum

from ..models import Event

router = APIRouter(tags=["events"])


@router.get(
    "",
    response_model_by_alias=True,
    response_model_exclude_none=True,
    response_model=ResponsePage[EventSchema],
)
def read_events(request: Request, session: Session, page: PageQuery):
    events = session.exec(select(Event)).all()
    return ResponsePage(
        results=events,
        request=request,
        status=StatusEnum.success,
        message="Successfully retrieved the model #Events",
        total_records=len(events),
        # TODO: passing the actual page query object gives a
        # pydantic validation error indicating that the field is not
        # a valid Page instance
        page=Page.model_validate(page.model_dump()),
    )


@router.get(
    "/{event_id}",
    response_model_by_alias=True,
    response_model_exclude_none=True,
    response_model=Response[EventSchema],
)
def find_event(request: Request, event_id: int):
    return Response(
        result=EventSchema(
            id=1,
            page="/dummy/path",
            agent="dummy-agent",
            ip_address=IPv4Address("127.0.0.1"),
            session_id="7e10c4b8-f9f7-4073-98a7-b6056c3d0cd6",
        ),
        request=request,
        status=StatusEnum.success,
        message="Processed successfully",
    )


@router.post(
    "",
    response_model=Response[EventSchema],
    response_model_by_alias=True,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    name="Create single event",
)
def create_event(request: Request, session: Session, payload: EventCreate):
    raw_obj = payload.model_dump()
    raw_obj["referrer"] = str(raw_obj["referrer"]) if raw_obj["referrer"] else None
    db_obj = Event.model_validate(raw_obj)
    try:
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
    except SQLAlchemyError as e_sql:
        session.rollback()
        request.state.logger.exception(
            "Database error: processing request %s",
            request.headers.get(constants.REQ_ID_HEADER),
            exc_info=e_sql,
        )
        raise HTTPException(
            status_code=500,
            detail=Response(
                request=request,
                status=StatusEnum.error,
                message="Internal server error",
            ).model_dump(exclude_none=True, exclude_unset=True),
        ) from None
    return Response(
        result=db_obj,
        request=request,
        status=StatusEnum.success,
        message="Event created successfully",
    )
