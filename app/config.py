from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    # Embedding model used for converting text chunks and queries into vectors
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM model served through Groq for answer generation
    llm_model: str = "llama-3.1-8b-instant"

    # Controls LLM randomness; lower is better for grounded RAG answers
    llm_temperature: float = 0.2

    # Local path where ChromaDB stores vector data
    vector_db_path: str = "data/vector_db"

    # ChromaDB collection name for stored knowledge chunks
    collection_name: str = "knowledge_base"

    # Default chunking configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Default number of chunks retrieved per query
    top_k: int = 5


config = AppConfig()