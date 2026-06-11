from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings
# Generate embeddings for document chunks using HuggingFace models
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)



