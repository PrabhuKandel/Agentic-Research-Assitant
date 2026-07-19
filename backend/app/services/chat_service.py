from uuid import UUID
from sqlalchemy.orm import Session
from app.models.chat import Chat, Message


def create_chat(db:Session)->Chat:
    """Create a new chat and return the Chat object."""
    new_chat = Chat(title="New Chat")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

def list_chats(db:Session)->list[Chat]:
    """Return all chats ordered by most recently updated."""
    return (
    db.query(Chat)
        .order_by(Chat.updated_at.desc())
        .all()
    )

def get_chat(db:Session, chat_id:UUID)->Chat|None:
    """Return a chat by its ID, or None if not found."""
    return db.query(Chat).filter(Chat.id == chat_id).first()

def delete_chat(db:Session, chat:Chat)->bool:
    """
    Delete one chat and all of its messages.

    Related messages are deleted automatically because the model
    relationship uses cascade delete and the foreign key has ON DELETE CASCADE.
    """
    db.delete(chat)
    db.commit()


def create_message(
    db:Session, chat:Chat, role:str, content:str
)->Message:
    """Create a new message in a chat and return the Message object."""
  
    new_message = Message(chat=chat, role=role, content=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message


