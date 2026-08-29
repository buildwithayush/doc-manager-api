from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.database import Base, engine

app =FastAPI()
app.include_router(api_router,prefix='/api/v1')
