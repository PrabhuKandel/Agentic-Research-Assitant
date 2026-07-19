from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.chat import (
    ChatCreateResponse,
    ChatDeleteResponse,
    ChatDetailResponse,
    ChatListResponse,
)
from app.api.schemas.rag import (
    ChatQueryResponse,
    ChatQueryRequest,
)

from app.db.session import get_db
from app.services.chat_service import (
    create_chat,
    create_message,
    delete_chat,
    get_chat,
    list_chats,

)
from app.services.rag_pipeline import run_rag_pipeline


router = APIRouter(prefix="/chats", tags=["chats"])


def create_chat_title(question: str) -> str:
    """
    Create a simple title using the first six words
    of the user's first question.
    """
    words = question.strip().split()

    if not words:
        return "New Chat"

    title = " ".join(words[:6])

    if len(words) > 6:
        title += "..."

    return title


@router.post("", response_model=ChatCreateResponse, status_code=status.HTTP_201_CREATED)
def create_new_chat(
    db: Session = Depends(get_db),
) -> ChatCreateResponse:
    """Create a new chat."""
    chat = create_chat(db)
    return chat


@router.get("", response_model=ChatListResponse)
def get_chats(
    db: Session = Depends(get_db),
) -> ChatListResponse:
    """Retrieve all chats."""
    chats = list_chats(db)
    return ChatListResponse(chats=chats)


@router.get("/{chat_id}", response_model=ChatDetailResponse)
def get_chat_by_id(
    chat_id: UUID,
    db: Session = Depends(get_db),
) -> ChatDetailResponse:
    """Retrieve one chat and its messages."""
    chat = get_chat(db, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    return chat


@router.delete("/{chat_id}", response_model=ChatDeleteResponse)
def remove_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
) -> ChatDeleteResponse:
    """Delete one chat and its messages."""
    chat = get_chat(db, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    delete_chat(db, chat)

    return ChatDeleteResponse(
        message="Chat deleted successfully.",
    )

@router.post("/{chat_id}/messages", response_model=ChatQueryResponse)
def send_message_to_chat(
    chat_id: UUID,
    request: ChatQueryRequest,
    db: Session = Depends(get_db),
) -> ChatQueryResponse:
    """Send a message to a chat and get the assistant's response."""
    chat = get_chat(db, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )
    
    is_first_message = len(chat.messages) == 0

    # Save user message to the database
    create_message(
        db=db,
        chat=chat,
        role="user",
        content=request.query,
    )

    # Run RAG pipeline to get the assistant's response
    response = run_rag_pipeline(request.query, db)

    # Save assistant message to the database
    create_message(
        db=db,
        chat=chat,
        role="assistant",
        content=response["answer"],
    )

    if is_first_message and chat.title == "New Chat":
        chat.title = create_chat_title(request.query)
        db.commit()
        db.refresh(chat)


    return ChatQueryResponse(**response)