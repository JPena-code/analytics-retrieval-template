from fastapi.routing import APIRouter

from . import events

__version__ = "1.0"
VERSION = f"v{__version__}"

router = APIRouter(prefix=f"/api/{VERSION}")

router.include_router(events.router, prefix="/event", tags=["events", VERSION])

__all__ = ["router"]
