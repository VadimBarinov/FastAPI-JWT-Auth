from fastapi import  FastAPI

from app.routers.users.router import router as users_router


app = FastAPI()


@app.get("/", summary="Начальная страница")
def home_page() -> dict:
    return {"message": "Hello, Index!"}


app.include_router(users_router)