import logging
from importlib import import_module
from typing import cast

import pymupdf4llm
from app.core.config import settings
from app.services.storage_services import minio_client

logger = logging.getLogger(__name__)

try:
    fitz = import_module("fitz")
except ImportError:
    fitz = import_module("pymupdf4llm")

class PDFExtractionService:

    @staticmethod
    def extract_text_from_minio_stream(object_path: str) -> str:
        response = None
        try:
            
            response = minio_client.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_path
            )
            file_bytes = response.read()

            if not file_bytes:
                logger.error("MinIO object %s is empty!", object_path)
                return ""
            
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            
             md_text = cast(str,pymupdf4llm.to_markdown(doc,page_chunks=False))
            return md_text

        finally:
            if response:
                response.close()
                response.release_conn()
