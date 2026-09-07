from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.services.storage_services import init_storage

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.TESTING:
        init_storage()

    yield


app =FastAPI(
    title="Document Management API",
    description="Enterprise-grade Document & File Management System",
    lifespan=lifespan
)
app.include_router(api_router,prefix='/api/v1')


