from app.models import Document
from sqlalchemy.orm import Session

from uuid import UUID
from pathlib import Path

def get_document(db:Session, document_id:UUID) -> Document|None:
    """Return one document by ID, or None if it does not exist."""
    return db.query(Document).filter(Document.id == document_id).first()


def list_documents(db:Session) -> list[Document]:
    """Return a list of all documents."""
    return db.query(Document).order_by(Document.created_at.desc()).all()

def delete_document(db:Session, document:Document) -> Document|None:
    """
    Delete one document from the database and remove its uploaded file.

    Related document chunks are deleted automatically because the model
    relationship uses cascade delete and the foreign key has ON DELETE CASCADE.
    """
    file_path = Path(document.file_path)

    try:
         # Stage the DB delete, but do not permanently commit yet.
         db.delete(document)
         db.flush()  # Flush the delete to the DB to ensure it succeeds before removing the file from disk.
        

    # Delete the file while the DB transaction is still open.
    # If this fails, the except block rolls back the DB delete.
    # If the file was already manually removed, do nothing.
         if file_path.exists():
            file_path.unlink(missing_ok=True)
            
         # Commit only after DB delete and file delete both succeeded.
         db.commit()
        
    except Exception:
         # Undo the DB delete if anything failed before commit.
        db.rollback()
        raise