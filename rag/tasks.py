import logging
from app.database import SessionLocal
from app.models.chunk_model import DocumentChunk
from app.models.document_model import Document
from rag.services.emdedding_service import EmbeddingService
from rag.services.pdf_service import PDFExtractionService
from rag.services.chunk_service import LangChainChunkService
logger = logging.getLogger(__name__)

def process_pdf_document_tasks(doc_id:int,object_path:str) -> None:
    
    db = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            logger.error(f"Background Task Failed: Document {doc_id} not found.")
            return
        
        text = PDFExtractionService.extract_text_from_minio_stream(object_path=object_path)

        chunks = LangChainChunkService.chunk_by_tokens(text=text)

        chunk_records = []
        for idx, chunk_content in enumerate(chunks):
            vector = EmbeddingService.get_embedding(chunk_content)
            chunk_obj = DocumentChunk(
                document_id=doc_id,
                chunk_index=idx,
                content=chunk_content,
                embedding=vector
            )
            chunk_records.append(chunk_obj)

        if chunk_records:
         db.add_all(chunk_records)
         doc.status = "processed"
         db.commit()
         
        logger.info(f'Document {doc_id} successfully processed and saved.') 

    except Exception as exc:
        db.rollback()
        logger.exception(f"Document {doc_id} processing failed: {str(exc)}")   

    finally:
        db.close()       