# backend/app/repositories/sql.py

from sqlalchemy.orm import Session
from app.models import Chat as ChatModel, Message as MessageModel
from .base import IMessageRepository, ChatNotFoundError
from datetime import datetime


class SQLMessageRepository(IMessageRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self) -> ChatModel:
        chat = ChatModel()
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def list_chats(self) -> list[ChatModel]:
        return self.db.query(ChatModel).order_by(ChatModel.created_at.asc()).all()

    def add_message(self, chat_id: int, role: str, content: str) -> MessageModel:
        chat = self.db.query(ChatModel).get(chat_id)
        if not chat:
            raise ChatNotFoundError(f"Chat {chat_id} not found")
        msg = MessageModel(chat_id=chat_id, role=role, content=content, timestamp=datetime.utcnow())
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_messages(self, chat_id: int) -> list[MessageModel]:
        chat = self.db.query(ChatModel).get(chat_id)
        if not chat:
            raise ChatNotFoundError(f"Chat {chat_id} not found")
        return (
            self.db.query(MessageModel)
            .filter(MessageModel.chat_id == chat_id)
            .order_by(MessageModel.timestamp.asc())
            .all()
        )