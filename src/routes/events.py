from ipaddress import IPv4Address

from fastapi import APIRouter, Request

from ..schemas import EventCreate, Response

router = APIRouter(tags=["events"])


@router.get(
    "/",
    response_model_by_alias=True,
    response_model_exclude_none=True,
    response_model=Response[EventCreate],
)
async def events(req: Request):
    return Response[EventCreate](
        data=[
            EventCreate(
                path="/dummy/path/",
                agent="dummy-agent",
                ip_address=IPv4Address("172.0.0.1"),
                session_id="dummy-session",
            ),
            EventCreate(
                path="/dummy/path/",
                agent="dummy-agent",
                ip_address=IPv4Address("172.0.0.1"),
                session_id="dummy-session",
            ),
        ],
        req=req,
    )
