from fastapi import HTTPException, Request, status
from fastapi.routing import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from config import constants
from depends import PageQuery, Session
from models import Event
from schemas import EventCreate, EventSchema, Page, Response, ResponsePage, StatusEnum

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
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    response_model=Response[EventSchema],
)
def find_event(request: Request, session: Session, event_id: int):
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Response(
                request=request,
                status=StatusEnum.error,
                message=f"Event with id {event_id} not found",
            ),
        )
    return Response(
        result=event,
        request=request,
        status=StatusEnum.success,
        message="Processed successfully",
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
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
