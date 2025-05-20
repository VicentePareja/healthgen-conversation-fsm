# backend/app/repositories/memory.py

from app.models import Chat as ChatModel, Message as MessageModel
from .base import IMessageRepository, ChatNotFoundError, ISlotRepository
from datetime import datetime, timedelta
from typing import List


class InMemoryMessageRepository(IMessageRepository):
    def __init__(self):
        self._chats: List[ChatModel] = []
        self._messages: List[MessageModel] = []
        self._next_chat_id = 1
        self._next_msg_id = 1

    def create_chat(self) -> ChatModel:
        chat = ChatModel(id=self._next_chat_id, created_at=datetime.utcnow())
        self._next_chat_id += 1
        self._chats.append(chat)
        return chat

    def list_chats(self) -> List[ChatModel]:
        return list(self._chats)

    def add_message(self, chat_id: int, role: str, content: str) -> MessageModel:
        if not any(c.id == chat_id for c in self._chats):
            raise ChatNotFoundError(f"Chat {chat_id} not found")
        msg = MessageModel(
            id=self._next_msg_id,
            chat_id=chat_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
        )
        self._next_msg_id += 1
        self._messages.append(msg)
        return msg

    def get_messages(self, chat_id: int) -> List[MessageModel]:
        if not any(c.id == chat_id for c in self._chats):
            raise ChatNotFoundError(f"Chat {chat_id} not found")
        return sorted(
            [m for m in self._messages if m.chat_id == chat_id],
            key=lambda m: m.timestamp,
        )
    
class InMemorySlotRepository(ISlotRepository):
    def get_next_slots(self, days: int, per_day: int) -> List[str]:
        slots: List[str] = []
        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        # default times for each day
        default_hours = [9, 11, 14]
        for day_offset in range(days):
            date = now + timedelta(days=day_offset)
            for hour in default_hours[:per_day]:
                slot_time = date.replace(hour=hour)
                slots.append(slot_time.isoformat())
        return slots