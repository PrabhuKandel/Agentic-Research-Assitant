from langchain_core.documents import Document
from .generation_service import generate_response
from .retrieval_service import retrieve_relevant_chunks

DEFAUL_TOP_K = 5

def run_rag_pipeline(query: str, top_k: int = DEFAUL_TOP_K) -> str:
    # Step 1: Retrieve relevant chunks from the vector database
    retrieved_results = retrieve_relevant_chunks(query, top_k=top_k)

    # Extract only Document objects from (Document, score) pairs
    retrieved_documents = [document for document, score in retrieved_results]

    # Step 2: Generate a response using the retrieved documents as context
    answer = generate_response(query, retrieved_documents)

    return {
        "query": query,
        "answer": answer,
        "sources": format_sources(retrieved_results)

    }

def format_sources(retrieved_results: list[tuple[Document, float]]) -> list[dict]:
    sources = []
    for document, score in retrieved_results:
        sources.append({
                "source_file": document.metadata.get("source_file"),
                "page": document.metadata.get("page"),
                "score": score,
                "preview": document.page_content,
        })
    return sources

if __name__ == "__main__":
    query = "What is finetuning?"

    result = run_rag_pipeline(query=query)

    print("Question:", result["query"])
    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for index, source in enumerate(result["sources"], start=1):
        print(f"\n--- Source {index} ---")
        print(source)
