from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown", ".docx"}


def load_document(file_path: str) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = path.suffix.lower()

    if file_extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {file_extension}")

    if file_extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif file_extension == ".docx":
        loader = Docx2txtLoader(str(path))

    else:
        loader = TextLoader(str(path), encoding="utf-8")

    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = path.name
        document.metadata["file_type"] = file_extension

    return documents
