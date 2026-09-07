from minio import Minio, S3Error
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.document_model import Document
from fastapi import status, HTTPException
from app.schemas.document_schema import DocumentUpdate
from app.services.storage_services import delete_file_from_minio


minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)

def create_document_with_file(
        db:Session,
        title:str,
        description:str | None,
        file_name:str,
        file_path:str,
        file_type:str,
        file_size:int,
        user_id:int
) -> Document:
    new_doc = Document(
        title = title,
        description=description,
        file_name = file_name,
        file_path = file_path,
        file_type = file_type,
        file_size=file_size,
        user_id=user_id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_user_document(db:Session,user_id:int,skip:int =0 ,limit:int = 20) -> list[Document]:
    return db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).offset(skip).limit(limit).all()

def get_document_by_id(db:Session,doc_id:int,user_id:int) -> Document:
    doc = db.query(Document).filter(Document.id == doc_id,Document.user_id == user_id).first()

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Document not found'
        )
    return doc

def update_document(
    db: Session,
    doc_id: int,
    user_id: int,
    doc_in: DocumentUpdate
) -> Document:
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user_id
    ).first()

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    update_data = doc_in.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update."
        )
    
    for key, value in update_data.items():
        setattr(doc, key, value)

    db.commit()
    db.refresh(doc)
    return doc

def delete_document(db: Session, doc_id: int, user_id: int) -> None:
    
    doc = get_document_by_id(db, doc_id, user_id)

    
    if doc.file_path:
        delete_file_from_minio(doc.file_path)

    
    db.delete(doc)
    db.commit()