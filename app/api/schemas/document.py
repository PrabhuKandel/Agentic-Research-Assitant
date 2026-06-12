from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    """Response body returned after a document is uploaded and ingested."""

    filename: str
    document_id: str
    message: str