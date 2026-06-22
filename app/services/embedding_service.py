from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings



@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
        """Load the embedding model once and reuse it across the app."""
        
        return HuggingFaceEmbeddings(
        model_name=settings.embedding_model
        )



