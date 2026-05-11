from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# Split documents into smaller chunks using RecursiveCharacterTextSplitter
def chunk_documents(
        documents: list[Document], 
        chunk_size: int = DEFAULT_CHUNK_SIZE,
          chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
          ) -> list[Document]:
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # Split LangChain documents while preserving their metadata
    return text_splitter.split_documents(documents)

if __name__ == "__main__":
    from app.services.document_loader import load_document
    from app.services.text_preprocessor import preprocess_documents

    # Load raw documents from the local uploads folder
    docs = load_document("data/uploads/AI Engineering.pdf")

    # Clean extracted text before splitting
    cleaned_docs = preprocess_documents(docs)

    # Split cleaned documents into smaller retrievable chunks
    chunks = chunk_documents(cleaned_docs)

    print(f"Total chunks: {len(chunks)}")
    print("Metadata:", chunks[1000].metadata)
    print("Preview:", chunks[1000].page_content)
