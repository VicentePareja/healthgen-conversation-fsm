# backend/app/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
    role = Column(String, nullable=False)               # "user" o "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class ConversationState(Base):
    """
    Persist the current FSM state and collected payload for each chat.
    We’ve broken out name, age, allergy, selected_slot into their own columns.
    """
    __tablename__ = "conversation_states"

    chat_id       = Column(Integer, ForeignKey("chats.id"), primary_key=True, index=True)
    state_name    = Column(String, nullable=False)
    name          = Column(String, nullable=True)
    age           = Column(Integer, nullable=True)
    allergy       = Column(Boolean, nullable=True)
    selected_slot = Column(String, nullable=True)
    payload       = Column(JSONB, nullable=False, default=dict)