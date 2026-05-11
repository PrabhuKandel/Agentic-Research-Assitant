from langchain_huggingface import HuggingFaceEmbeddings

# Generate embeddings for document chunks using HuggingFace models
def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=model_name)


if __name__ == "__main__":
    embeddings = get_embedding_model()

    sample_text = "Artificial Intelligence is transforming software engineering."

    vector = embeddings.embed_query(sample_text)

    print(f"Embedding dimensions: {len(vector)}")
    print("Vector preview:", vector)

