from langchain_core.documents import Document
from app.services.vector_store import load_vector_store
from app.config import config



def retrieve_relevant_chunks(query: str, top_k: int = config.top_k) -> list[tuple[Document, float]]:
    # Load the existing vector store
    vector_store = load_vector_store()

    # Perform a similarity search to retrieve relevant document chunks based on the query
    results = vector_store.similarity_search_with_score(query, k=top_k)

    return results
