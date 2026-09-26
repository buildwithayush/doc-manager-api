import logging

from app.database import SessionLocal
from app.models.chunk_model import DocumentChunk
from app.models.document_model import Document
from rag.services.emdedding_service import EmbeddingService
from rag.services.markdown_chunk_service import MarkdownChunkService
from rag.services.pdf_service import PDFExtractionService

logger = logging.getLogger(__name__)


def process_pdf_document_tasks(doc_id: int, object_path: str) -> None:
    db = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            logger.error("Background Task Failed: Document %s not found.", doc_id)
            return

        md_content = PDFExtractionService.extract_text_from_minio_stream(object_path=object_path)

        chunks = MarkdownChunkService.split_by_headers(markdown_text=md_content)

        chunk_records = []
        for idx, chunk in enumerate(chunks):
            raw_content = chunk.page_content.strip()
            if not raw_content:
                continue

            header_values = [str(val).strip() for val in chunk.metadata.values() if str(val).strip()]
            header_prefix = " > ".join(header_values)
            enriched_text = f"[{header_prefix}]\n{raw_content}" if header_prefix else raw_content

            vector = EmbeddingService.get_embedding(enriched_text)
            chunk_obj = DocumentChunk(
                document_id=doc_id,
                chunk_index=idx,
                content=enriched_text,
                embedding=vector,
            )
            chunk_records.append(chunk_obj)
            
        if chunk_records:
            db.add_all(chunk_records)
            db.commit()

        logger.info("Document %s successfully processed and saved.", doc_id)

    except Exception as exc:
        db.rollback()
        logger.exception("Document %s processing failed: %s", doc_id, exc)

    finally:
        db.close()
