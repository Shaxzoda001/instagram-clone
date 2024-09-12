from fastapi import APIRouter

follow_router = APIRouter(prefix="/followers", tags=["followers"])

@follow_router.get("/")
async def get_followers():
    return {"message": "Followers page"}
