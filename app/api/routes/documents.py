from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.api.schemas.document import (
    DocumentDeleteResponse,
    DocumentListResponse,
    DocumentResponse,
)
from app.db.session import get_db
from app.services.document_service import (
    delete_document,
    get_document,
    list_documents,
)


router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("", response_model=DocumentListResponse)
def get_documents(db: Session = Depends(get_db))-> DocumentListResponse:
    """Retrieve a list of all documents."""
    documents = list_documents(db)
    # Pydantic models require keyword arguments, so documents=documents tells it which field to fill since there can be multiple fields.
    return DocumentListResponse(documents=documents)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_by_id(
    document_id: UUID,
    db:Session = Depends(get_db)
) -> DocumentResponse:
    """Retrieve a single document by ID."""
    document = get_document(db, document_id)
    if  document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def remove_document(
    document_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentDeleteResponse:
    """Delete one uploaded document and its stored chunks."""

    document = get_document(db, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    delete_document(db, document)

    return DocumentDeleteResponse(
        document_id=document_id,
        message="Document deleted successfully.",
    )