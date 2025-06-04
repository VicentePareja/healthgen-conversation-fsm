# backend/app/repositories/base.py

from abc import ABC, abstractmethod
from typing import List
from app.models import Chat as ChatModel, Message as MessageModel


class ChatNotFoundError(Exception):
    """Raised when a chat ID does not exist."""
    pass


class IMessageRepository(ABC):
    @abstractmethod
    def create_chat(self) -> ChatModel:
        """Crea un nuevo chat y devuelve el objeto Chat."""
        ...

    @abstractmethod
    def list_chats(self) -> List[ChatModel]:
        """Devuelve todos los chats existentes."""
        ...

    @abstractmethod
    def add_message(self, chat_id: int, role: str, content: str) -> MessageModel:
        """
        Añade un mensaje al chat.
        Lanza ChatNotFoundError si el chat no existe.
        """
        ...

    @abstractmethod
    def get_messages(self, chat_id: int) -> List[MessageModel]:
        """
        Recupera todos los mensajes de un chat, ordenados por timestamp ascendente.
        Lanza ChatNotFoundError si el chat no existe.
        """
        ...

class ISlotRepository(ABC):
    @abstractmethod
    def get_next_slots(self, days: int, per_day: int) -> List[str]:
        """
        Return up to `per_day` ISO-timestamp slots for each of the next `days` days.
        """
        ...