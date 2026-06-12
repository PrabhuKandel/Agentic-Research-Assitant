from pathlib import Path as FilePath

from app.db.session import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Path, UploadFile, status

from app.api.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.api.schemas.document import DocumentUploadResponse
from app.services.file_storage import save_upload_file
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
def upload_document(
    file:UploadFile,
    db:Session = Depends(get_db)
    ) -> DocumentUploadResponse:
 
    try:
        saved_file_path, original_filename = save_upload_file(file)
      
        result = ingest_document(str(saved_file_path),original_filename, db)

        return DocumentUploadResponse(
            filename=original_filename,
            document_id=result["document_id"],
            message="Document uploaded and ingested successfully."
        )
    
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
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
def query_chat(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
) -> ChatQueryResponse:
    """Answer a user question using the RAG pipeline."""

    try:
        result = run_rag_pipeline(request.query, db)

        return ChatQueryResponse(**result)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {error}",
        )

  