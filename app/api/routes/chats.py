from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.chat import (
    ChatCreateResponse,
    ChatDeleteResponse,
    ChatDetailResponse,
    ChatListResponse,
)
from app.db.session import get_db
from app.services.chat_service import (
    create_chat,
    delete_chat,
    get_chat,
    list_chats,
)


router = APIRouter(prefix="/chats", tags=["chats"])

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