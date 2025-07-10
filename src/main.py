from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.router import api_router
from core.config import settings
from db.session import init_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield


app = FastAPI(
    title="nori contacts server",
    version="0.1.0",
    description="A robust backend API using FastAPI.",
    docs_url="/docs" if settings.APP_MODE != "prod" else None,
    redoc_url="/redoc" if settings.APP_MODE != "prod" else None,
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the nori-contacts-server!"}
