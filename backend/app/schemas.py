# backend/app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class Item(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Chat(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class MessageCreate(MessageBase):
    """Lo que envía el cliente al POSTear un mensaje."""
    pass


class Message(MessageBase):
    id: int
    chat_id: int
    timestamp: datetime

    class Config:
        orm_mode = True