import logging
import os
from importlib import import_module
from app.core.config import settings
from app.services.storage_services import minio_client

logger = logging.getLogger(__name__)

try:
    fitz = import_module("fitz")
except ImportError:
    fitz = import_module("pymupdf")

EXTRACTED_DOC_DIR = os.path.join(os.getcwd(), "docs", "extracted")
os.makedirs(EXTRACTED_DOC_DIR, exist_ok=True)

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

            extracted_pages: list[str] = []

            
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                total_pages = len(doc)
                logger.info("Processing PDF with %s pages...", total_pages)

                for page_num in range(total_pages):
                    page = doc.load_page(page_num)
                    page_text = page.get_text("text")
                    
                    if page_text and page_text.strip():
                        extracted_pages.append(page_text.strip())

            full_text = "\n\n".join(extracted_pages)
            logger.info("Extracted %s characters.", len(full_text))
            return full_text

        finally:
            if response:
                response.close()
                response.release_conn()

    @staticmethod
    def save_extracted_text(doc_id: int, text: str) -> str:
        file_path = os.path.join(EXTRACTED_DOC_DIR, f"{doc_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info("File saved to %s", file_path)
        return file_path