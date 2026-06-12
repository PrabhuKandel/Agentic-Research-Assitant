from langchain_core.documents import Document as LangchainDocument
from sqlalchemy.orm import Session
from app.models import DocumentChunk
from app.services.vector_store import load_vector_store
from app.config import settings
from app.services.embedding_service import get_embedding_model



def retrieve_relevant_chunks(
        query: str,
        db:Session,
        top_k: int = settings.top_k) -> list[tuple[LangchainDocument, float]]:
    
    embedding_model = get_embedding_model()
    query_embedding = embedding_model.embed_query(query)

    distance = DocumentChunk.embedding.cosine_distance(query_embedding).label("score")

    rows = (
        db.query(DocumentChunk, distance)
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    results=[]

    for chunk, score in rows:
        doc = LangchainDocument(
            page_content=chunk.content,
            metadata={
                "source_file": chunk.source_file,
                "source_type": chunk.source_type,
                "page": chunk.page,
                "section": chunk.section,
                "document_id": str(chunk.document_id),
                "chunk_id": str(chunk.id),
            }
        )
        results.append((doc, float(score)))


    return results
