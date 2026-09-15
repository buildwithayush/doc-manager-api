from sqlalchemy.orm import Session
from app.models.chunk_model import DocumentChunk
from rag.services.emdedding_service import EmbeddingService

class RetrievalService:
    @staticmethod
    def get_relevant_chunks(
        db: Session,
        query: str,
        top_k: int = 5,
        document_id: int | None = None
    ) -> list[str]:
        # Step 1: Generate Query Embedding
        query_vector = EmbeddingService.get_embedding(query)

        # Step 2: Query pgvector
        query_builder = db.query(DocumentChunk).order_by(
            DocumentChunk.embedding.cosine_distance(query_vector)
        )
        # Optional: If user want to chat with a specific document, filter by document_id
        if document_id is not None and document_id > 0:
            query_builder = query_builder.filter(DocumentChunk.document_id == document_id)

        matched_chunks = query_builder.limit(top_k).all()

        return [chunk.content for chunk in matched_chunks]