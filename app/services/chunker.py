from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import config


# Split documents into smaller chunks using RecursiveCharacterTextSplitter
def chunk_documents(
        documents: list[Document], 
        chunk_size: int = config.chunk_size,
          chunk_overlap: int = config.chunk_overlap
          ) -> list[Document]:
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # Split LangChain documents while preserving their metadata
    return text_splitter.split_documents(documents)

