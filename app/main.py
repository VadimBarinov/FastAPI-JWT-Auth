from fastapi import  FastAPI

from app.routers.users.router import router as users_router


app = FastAPI()


@app.get("/", summary="Начальная страница")
def home_page() -> dict:
    return {"message": "Начальная страница"}


app.include_router(users_router)