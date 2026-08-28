from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints import auth

router = APIRouter()

router.include_router(health.router,prefix='/health')
router.include_router(auth.router,prefix='/auth',tags=['Authentication'])