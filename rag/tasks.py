import logging
from app.database import SessionLocal
from app.models.document_model import Document
from rag.services.pdf_service import PDFExtractionService
from rag.services.chunk_service import ChunkService
logger = logging.getLogger(__name__)

def process_pdf_document_tasks(doc_id:int,object_path:str) -> None:
    
    db = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            logger.error(f"Background Task Failed: Document {doc_id} not found.")
            return
        
        text = PDFExtractionService.extract_text_from_minio_stream(object_path=object_path)

        PDFExtractionService.save_extracted_text(doc_id=doc_id,text=text)

        chunks = ChunkService.chunk_text(text=text, chunk_size=1000, chunk_overlap=200)
        total_chunks = len(chunks)
        logger.info("Total Chunks: %s", total_chunks)

        logger.info("-------------------- CHUNK INSPECTION (TOP 10) --------------------")
        inspect_limit = min(10, total_chunks)
        for idx in range(inspect_limit):
            chunk_preview = chunks[idx]
            logger.info("\n🔹 [CHUNK #%s] | Length: %s chars", idx + 1, len(chunk_preview))
            logger.info('"%s ... [TRUNCATED] ... %s"', chunk_preview[:150], chunk_preview[-100:])

        if total_chunks > 10:
            logger.info("\n... and %s more chunks remaining.", total_chunks - 10)
        logger.info("-------------------------------------------------------------------\n")
       
        doc.status = 'processed'
        db.commit()
        logger.info(f'Document {doc_id} successfully processed and saved.') 

    except Exception as exc:
        db.rollback()
        logger.exception(f"Document {doc_id} processing failed: {str(exc)}")   

    finally:
        db.close()       