from shutil import copyfileobj
from pathlib import Path as FilePath

from fastapi import FastAPI, HTTPException, Path, UploadFile, status

from app.api.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.api.schemas.document import DocumentUploadResponse
from app.services.ingestion_pipeline import ingest_document
from app.services.rag_pipeline import run_rag_pipeline

app = FastAPI(

    title="Agentic Research Assistant API",
    description="API for ingesting documents and querying the agentic research assistant.",
    version="1.0.0",
)

@app.get("/")
def health_check()->dict[str, str]:
    return {
        "status": "ok", 
        "message": "Agentic Research Assistant API is running."
        }

@app.post(
        "/documents/upload",
        response_model = DocumentUploadResponse,
        status_code = status.HTTP_201_CREATED,
        )
def upload_document(file:UploadFile) -> DocumentUploadResponse:

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename."
        )
    
    upload_dir = FilePath("data/uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    try:
        with file_path.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        ingest_document(str(file_path))

        return DocumentUploadResponse(
            filename=file.filename,
            message="Document uploaded and ingested successfully."
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {e}",
        )
    
    finally:
        file.file.close()


@app.post(
    "/chat/query",
    response_model=ChatQueryResponse,
    status_code=status.HTTP_200_OK,
)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    """Answer a user question using the RAG pipeline."""

    try:
        result = run_rag_pipeline(request.query)

        return ChatQueryResponse(**result)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {error}",
        )

  