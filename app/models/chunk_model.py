from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from pgvector.sqlalchemy import Vector

if TYPE_CHECKING:
    from app.models.document_model import Document

class DocumentChunk(Base):
      __tablename__ = "document_chunks"

      id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
      document_id : Mapped[Integer] = mapped_column(Integer,ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False)

      chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

      content: Mapped[str] = mapped_column(Text, nullable=False)

      embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)

      created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

      document: Mapped['Document'] = relationship("Document", back_populates="chunks")