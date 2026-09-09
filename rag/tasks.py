import logging
from app.database import SessionLocal
from app.models.document_model import Document
from rag.services.pdf_service import PDFExtractionService

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

        doc.status = 'processed'
        db.commit()
        logger.info(f'Document {doc_id} successfully processed and saved.') 

    except Exception as exc:
        db.rollback()
        logger.exception(f"Document {doc_id} processing failed: {str(exc)}")   

    finally:
        db.close()       