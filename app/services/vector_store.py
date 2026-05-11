from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.services.embedding_service import get_embedding_model

DEFAULT_VECTOR_DB_PATH = "data/vector_db"
DEFAULT_COLLECTION_NAME = "knowledge_base"

def create_vector_store(
        documents: list[Document], 
        collection_name: str = DEFAULT_COLLECTION_NAME, 
        persist_directory: str = DEFAULT_VECTOR_DB_PATH
        ) -> Chroma:
    # Initialize the embedding model
    embedding_model = get_embedding_model()

    # Create a Chroma vector store with the specified collection name and path
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name=collection_name,
        persist_directory=persist_directory
    )


    return vector_store

def load_vector_store(
        collection_name: str = DEFAULT_COLLECTION_NAME, 
        persist_directory: str = DEFAULT_VECTOR_DB_PATH
        ) -> Chroma:
    
    # Load an existing Chroma vector store from the specified collection name and path
    embedding_model = get_embedding_model()
    return Chroma(collection_name=collection_name, persist_directory=persist_directory, embedding_function=embedding_model)


if __name__ == "__main__":
    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        "What is fine tuning?",
        k=3,
    )

    print(f"Retrieved results: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Metadata:", result.metadata)
        print("Preview:", result.page_content[:1000])