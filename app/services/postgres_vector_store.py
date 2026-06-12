from pathlib import Path

from langchain_core.documents import Document as LangchainDocument
from sqlalchemy.orm import Session

from app.models import Document, DocumentChunk, DocumentStatus
from app.services.embedding_service import get_embedding_model


def store_document_chunks(
    db:Session,
    file_path:str,
    original_filename:str,
    chunks:list[LangchainDocument]

)->Document:

    # Create a new document record in the database
    document = Document(
        original_filename=original_filename,
        file_path=file_path,
        file_type=Path(file_path).suffix.lstrip("."),
        status=DocumentStatus.PROCESSING.value,
    )
    db.add(document)
    db.flush()  # Flush to get the document ID for the chunks


    embedding_model = get_embedding_model()
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)

    # Create document chunk records for each chunk
    for index, chunk in enumerate(chunks):
        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk.page_content,
            embedding=embeddings[index],  # Use the computed embedding
            source_file=chunk.metadata.get("source_file", Path(file_path).name),
            source_type=chunk.metadata.get("file_type", document.file_type),
            page=chunk.metadata.get("page"),
            section=chunk.metadata.get("section"),
        )
        db.add(document_chunk)

    document.status = DocumentStatus.READY.value

    db.commit()
    db.refresh(document)

    return document

  
