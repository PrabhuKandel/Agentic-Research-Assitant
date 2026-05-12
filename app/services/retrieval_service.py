from langchain_core.documents import Document
from app.services.vector_store import load_vector_store

DEFAULT_TOP_K = 5

def retrieve_relevant_chunks(query: str, top_k: int = DEFAULT_TOP_K) -> list[tuple[Document, float]]:
    # Load the existing vector store
    vector_store = load_vector_store()

    # Perform a similarity search to retrieve relevant document chunks based on the query
    results = vector_store.similarity_search_with_score(query, k=top_k)

    return results

if __name__ == "__main__":
    query = "What is Spherical linear interpolation?"
    retrieved_chunks = retrieve_relevant_chunks(query)

    print(f"Retrieved {len(retrieved_chunks)} relevant chunks for query: '{query}'")

    for index, (chunk, score) in enumerate(retrieved_chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(f"Distance Score: {score:.4f}")
        print("Metadata:", chunk.metadata)
        print("Preview:", chunk.page_content[:1000])