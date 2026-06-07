from langchain_huggingface import HuggingFaceEmbeddings
from app.config import config
# Generate embeddings for document chunks using HuggingFace models
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.embedding_model)



