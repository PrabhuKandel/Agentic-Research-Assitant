import re
from langchain_core import documents
from langchain_core.documents import Document


# Preprocess loaded LangChain documents by cleaning extracted text
def preprocess_documents(documents: list[Document]) -> list[Document]:
    cleaned_docs = []


    for document in documents:
    # Remove extra whitespace
        cleaned_content = clean_content(document.page_content)
        document.page_content = cleaned_content
        cleaned_docs.append(document)

    return cleaned_docs


# Clean extracted content using regex normalization
def clean_content(content: str) -> str:

    # Replace multiple whitespaces/newlines/tabs with single space and trim leading/trailing whitespace
    return re.sub(r"\s+", " ", content).strip()


if __name__ == "__main__":
    from app.services.document_loader import load_document

    docs = load_document("data/uploads/AI Engineering.pdf")
    print("Original Documents:", docs[0].page_content[:500])  # Print first 500 characters of original content
    cleaned_docs = preprocess_documents(docs)
    print("Cleaned Documents:", cleaned_docs[0].page_content[:500])  # Print first 500 characters of cleaned content
