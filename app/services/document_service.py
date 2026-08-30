from sqlalchemy.orm import Session
from app.models.document_model import Document
from fastapi import status,HTTPException
from app.schemas.document_schema import DocumentCreate,DocumentUpdate

def create_document(db:Session,doc_in:DocumentCreate,user_id:int) -> Document:
    new_doc = Document(
        title = doc_in.title,
        description = doc_in.description,
        user_id = user_id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc

def get_user_document(db:Session,user_id:int,skip:int =0 ,limit:int = 20) -> list[Document]:
    return db.query(Document).filter(Document.user_id == user_id).offset(skip).limit(limit).all()

def get_document_by_id(db:Session,doc_id:int,user_id:int) -> Document:
    doc = db.query(Document).filter(Document.id == doc_id,Document.user_id == user_id).first()

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Document not found'
        )
    return doc

def update_document(db:Session,doc_id,user_id:int,doc_in:DocumentUpdate) -> Document:
    doc = get_document_by_id(db=db,doc_id=doc_id,user_id=user_id)
    update_data = doc_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doc, key, value)

    db.add(doc)
    db.commit()
    db.refresh(doc)   

    return doc

def delete_document(db:Session,doc_id:int,user_id:int) -> None:
    doc = get_document_by_id(db=db,doc_id=doc_id,user_id=user_id)
    db.delete(doc)
    db.commit()
