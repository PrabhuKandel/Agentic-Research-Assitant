from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "Healthcare RAG Assistant"
    environment: str = "development"

    groq_api_key: str
    llm_model: str = "llama-3.1-8b-instant"
    llm_temperature: float = 0.2

    vector_db_path: str = "./data/vector_db"
    chroma_collection_name: str = "knowledge_base"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    database_url: str
    upload_dir: str = "data/uploads"
    max_upload_size_mb: int = 20

    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = AppSettings()