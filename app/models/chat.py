from enum import Enum
from tkinter import Message
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.db.base import Base

from sqlalchemy import String,Text, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MessageRole(str, Enum):
  
    USER = "user"
    ASSISTANT = "assistant"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="New Chat")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # One chat can have many messages.
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
    )


    class Message(Base):
        __tablename__ = "messages"

        id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
        chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id"), nullable=False)
        role: Mapped[str] = mapped_column(String(20), nullable=False)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )


        # Many messages belong to one chat.
        chat: Mapped["Chat"] = relationship(back_populates="messages")
