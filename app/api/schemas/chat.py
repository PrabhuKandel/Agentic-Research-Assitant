from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
    "from_attributes": True
}

class ChatListResponse(BaseModel):
    chats: list[ChatResponse] 

class MessageResponse(BaseModel):
    id: UUID
    chat_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = {
    "from_attributes": True
}


class MessageListResponse(BaseModel):
    messages: list[MessageResponse]


class ChatDetailResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse]


class ChatCreateResponse(BaseModel):
    id: UUID
    title: str


class ChatDeleteResponse(BaseModel):
    message: str


class MessageCreateRequest(BaseModel):
    content: str


class MessageCreateResponse(BaseModel):
    answer: str