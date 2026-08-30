from app.services.document_service import create_document,get_user_document,get_document_by_id
from app.services.document_service import delete_document ,update_document
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentCreate,DocumentResponse,DocumentUpdate
from fastapi import APIRouter,Depends,status,Query
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user_model import User

router = APIRouter()

@router.post('/',response_model=DocumentResponse,status_code=status.HTTP_201_CREATED)
def create_new_document(
    doc_in: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_document(db=db, doc_in=doc_in, user_id=current_user.id)

@router.get('/', response_model=list[DocumentResponse])
def get_all_documents(db:Session = Depends(get_db),skip:int = Query(0,ge=0),limit: int = Query(20, ge=1, le=100),  current_user:User= Depends(get_current_user)):
    return get_user_document(db=db,user_id=current_user.id,skip=skip,limit=limit)

@router.get('/{id}',response_model=DocumentResponse)
def get_single_document(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_document_by_id(doc_id=id,user_id=current_user.id,db=db)

@router.patch('/{id}',response_model=DocumentResponse)
def update_single_document(doc_id:int,doc_in:DocumentUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return update_document(db=db,doc_id=doc_id,user_id=current_user.id,doc_in=doc_in)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_single_document(id:int,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
     delete_document(db=db,doc_id=id,user_id=current_user.id)
     return None