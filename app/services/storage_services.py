from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from fastapi import UploadFile, HTTPException, status
import uuid
from sqlalchemy.orm import Session
from app.models.document_model import Document
import logging


logger = logging.getLogger(__name__)

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg','docx'}
MAX_FILE_SIZE = 10*1024*1024

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

def validate_file(file:UploadFile) -> None:
    filename = file.filename or ""
    ext = filename.rsplit(".",1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"

        )

def upload_file_to_minio(file:UploadFile,user_id:int) -> tuple[str,int]:
    validate_file(file=file)

    filename = file.filename or ""
    file_ext = filename.rsplit(".", 1)[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    object_name = f"users/{user_id}/{unique_filename}"

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 10 MB limit."
        )

    try:
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=object_name,
            data=file.file,
            length=file_size,
            content_type=file.content_type or "application/octet-stream"
        )
    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Storage upload failed: {str(err)}"
        ) from err

    return object_name, file_size


def delete_file_from_minio(object_path:str):
    try:
        minio_client.remove_object(bucket_name=settings.MINIO_BUCKET_NAME,object_name=object_path)

    except S3Error as err:
        logger.error(f"Failed to delete {object_path} from MinIO: {err}")

def get_file_from_minio(object_path:str):
    try:
        minio_client.get_object(bucket_name=settings.MINIO_BUCKET_NAME,object_name=object_path)

    except S3Error as err:
            logger.error(f"Failed to get {object_path} from MinIO: {err}")


        