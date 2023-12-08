from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router, tags=["Items"])
app.include_router(users_router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_pangolin():
    return {"message": "Привет, ящеры!"}


@app.get("/hello")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello, {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
