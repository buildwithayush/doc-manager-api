from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import documents
from app.api.v1.endpoints import chat

router = APIRouter()

router.include_router(health.router,prefix='/health')
router.include_router(auth.router,prefix='/auth',tags=['Authentication'])
router.include_router(documents.router,prefix='/documents',tags=['Documents'])
router.include_router(chat.router,prefix='/chat',tags=['RAG Chat'])