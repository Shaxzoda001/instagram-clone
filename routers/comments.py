from fastapi import APIRouter

comments_router = APIRouter(prefix="/comments", tags=["comments"])

@comments_router.get("/")
async def get_comments():
    return {"message": "Comments page"}