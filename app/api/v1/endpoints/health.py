from fastapi import APIRouter
from app.services.storage_services import check_storage_health

router = APIRouter()

@router.get('/')
def health_check():
    return {
        'status':'ok'
    }

@router.get('/storgae')
def storage_health():
    is_healthy = check_storage_health()
    return {
        'storage':'MiniIO S3',
        'connected':is_healthy
    }