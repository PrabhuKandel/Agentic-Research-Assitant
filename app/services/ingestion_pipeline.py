from pathlib import Path

from app.services.chunker import chunk_documents
from app.services.document_loader import load_document
from app.services.text_preprocessor import preprocess_documents
from app.services.vector_store import create_vector_store

def ingest_document(file_path:str)->dict:

    #validate the document path early so ingestion fails with a clear error
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load raw docuement pages/content using the document loader
    documents = load_document(file_path)

    # Clean extracted text before chunking
    cleaned_documents = preprocess_documents(documents)


    # Split cleaned documents into smaller retrievable chunks
    chunks = chunk_documents(cleaned_documents)

    # Store chunks and embeddings in the vector database
    create_vector_store(chunks)

    return {
        "source_file": path.name,
        "loaded_documents": len(documents),
        "chunks_created": len(chunks),
        "status": "success",
    }

