from fastapi import FastAPI
from routers.auth import auth_router
# from routers.post import posts_router
from schemas import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
# app.include_router(posts_router)

@app.get("/")
async def root():
    return {"Hello": "World"}
