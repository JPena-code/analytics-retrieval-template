from fastapi import APIRouter

from .events import router as events_router

__version__ = "1.0"
VERSION = f"v{__version__}"

router = APIRouter(prefix=f"/api/v{VERSION}")

router.include_router(events_router, prefix="/events", tags=["events", VERSION])

__all__ = ["router"]
