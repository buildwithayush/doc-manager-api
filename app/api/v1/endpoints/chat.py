from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat_schema import ChatRequest,ChatResponse
from rag.services.llm_service import LLMService
from rag.services.retrieval_service import RetrievalService
router = APIRouter()

@router.post('',response_model=ChatResponse,status_code=status.HTTP_200_OK)
def chat_with_documents(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):

    chunks = RetrievalService.get_relevant_chunks(
        db=db,
        query=payload.question,
        top_k=3,
        document_id=payload.document_id
    )

    # 2. Generate Answer via Ollama LLM
    ai_answer = LLMService.generate_answer(
        query=payload.question,
        context_chunks=chunks
    )

    # 3. Return structured response
    return ChatResponse(
        question=payload.question,
        answer=ai_answer,
        retrieved_chunks_count=len(chunks),
        context_used=chunks
    )

