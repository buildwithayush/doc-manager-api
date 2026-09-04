from minio import Minio
from minio.error import S3Error
from app.core.config import settings

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

def init_storage():
    try:
        found = minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

    except S3Error as err:
        raise err

def check_storage_health() -> bool:
    try:
        return minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
    except Exception:
        return False

    
        