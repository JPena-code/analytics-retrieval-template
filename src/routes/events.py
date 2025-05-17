from fastapi import APIRouter

router = APIRouter(tags=["events"])


@router.get("/")
async def events():
    pass
