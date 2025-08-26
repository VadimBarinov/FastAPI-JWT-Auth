import uvicorn
from fastapi import  FastAPI

from app.routers.auth.router import router as auth_router


app = FastAPI()


@app.get("/", summary="Начальная страница")
def home_page() -> dict:
    """
    # Домашняя страница
    """
    return {"message": "Hello, Index!"}


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8080, reload=True)