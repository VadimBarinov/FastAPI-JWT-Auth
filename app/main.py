import uvicorn
from fastapi import  FastAPI

from app.routers.users.router import router as users_router


app = FastAPI()


@app.get("/", summary="Начальная страница")
def home_page() -> dict:
    return {"message": "Hello, Index!"}


app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8080, reload=True)