from enum import Enum
from uuid import UUID, uuid4

from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import settings
from app.db.base import Base


class DocumentStatus( Enum):
    """Enumeration of possible document statuses."""

    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class Document( Base):
    """Stores one uploaded documents"""

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column( primary_key=True, default=uuid4 )
    original_filename: Mapped[str]  = mapped_column( String(255), nullable=False )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # Tracks whether the document is uploaded, processing, ready, failed, or archived.
    status: Mapped[str] = mapped_column(
         String(20), 
         nullable=False,
         default=DocumentStatus.UPLOADED.value 
           )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda:datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc),
        nullable=False,
    )

    # One document can have many chunks.
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunk( Base):
    """Stores one chunk of document text and its vector embedding."""

    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # pgvector column. With all-MiniLM-L6-v2, this becomes vector(384).
    embedding: Mapped[list[float]] = mapped_column(
        Vector(settings.embedding_dimension),
        nullable=False,
    )

    source_file: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Many chunks belong to one document.
    document: Mapped["Document"] = relationship(back_populates="chunks")

    
