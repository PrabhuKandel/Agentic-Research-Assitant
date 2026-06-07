from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.services.embedding_service import get_embedding_model
from app.config import config


def create_vector_store( documents: list[Document]) -> Chroma:
    # Initialize the embedding model
    embedding_model = get_embedding_model()

    # Create a Chroma vector store with the specified collection name and path
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name=config.collection_name,
        persist_directory=config.vector_db_path
    )


    return vector_store

def load_vector_store( ) -> Chroma:
    
    # Load an existing Chroma vector store from the specified collection name and path
    embedding_model = get_embedding_model()
    return Chroma(collection_name=config.collection_name, persist_directory=config.vector_db_path, embedding_function=embedding_model)


