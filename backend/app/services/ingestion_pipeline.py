from pathlib import Path

from sqlalchemy.orm import Session

from app.services.chunker import chunk_documents
from app.services.document_loader import load_document
from app.services.text_preprocessor import preprocess_documents
from app.services.postgres_vector_store import store_document_chunks

def ingest_document(file_path:str,original_filename:str, db:Session)->dict:

    #validate the document path early so ingestion fails with a clear error
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load raw docuement pages/content using the document loader
    documents = load_document(file_path)

    # Some loaders can return an empty list for unreadable or empty documents.
    if not documents:
        raise ValueError("No readable content found in the document.")


    # Clean extracted text before chunking
    cleaned_documents = preprocess_documents(documents)

    # A document can load successfully but still contain no extractable text,
    # for example scanned PDFs or image-only PDFs.
    has_readable_text = any(
        document.page_content.strip()
        for document in cleaned_documents
    )

    if not has_readable_text:
        raise ValueError("Document does not contain readable text.")


    # Split cleaned documents into smaller retrievable chunks
    chunks = chunk_documents(cleaned_documents)

        # If chunking produces nothing, there is nothing useful to embed or store.
    if not chunks:
        raise ValueError("No chunks could be created from the document.")


    # Store chunks and embeddings in the vector database
    stored_document = store_document_chunks(db, file_path, original_filename, chunks)

    return {
        "document_id": str(stored_document.id),
        "source_file": path.name,
        "loaded_documents": len(documents),
        "chunks_created": len(chunks),
        "status": stored_document.status,
    }

