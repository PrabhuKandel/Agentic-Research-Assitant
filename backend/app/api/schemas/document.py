from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response body returned after a document is uploaded and ingested."""

    filename: str
    document_id: str
    message: str

class DocumentResponse(BaseModel):
    """Response body for a document retrieval request."""

    id:UUID
    original_filename: str
    file_path: str
    file_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    # Allows Pydantic to serialize SQLAlchemy model objects directly.
    model_config = {
        "from_attributes": True,
    }

class DocumentListResponse(BaseModel):
    """Response body for a request that retrieves a list of documents."""

    documents: list[DocumentResponse]


class DocumentDeleteResponse(BaseModel):
    """Response body returned after a document is deleted."""

    document_id: UUID
    message: str