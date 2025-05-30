from ipaddress import IPv4Address

from fastapi import APIRouter

from ..schemas import EventCreate, Response

router = APIRouter(tags=["events"])


@router.get("/", response_model_by_alias=True, response_model_exclude_none=True)
async def events() -> Response[EventCreate]:
    return Response[EventCreate](
        data=EventCreate(
            path="/dummy/path/",
            agent="dummy-agent",
            ip_address=IPv4Address("172.0.0.1"),
            session_id="dummy-session",
        ),
        metadata={"TODO": "Add real metadata about the response"},
    )
