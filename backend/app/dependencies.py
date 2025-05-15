# backend/app/dependencies.py

import os
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .repositories.base import IMessageRepository, ChatNotFoundError
from .repositories.sql import SQLMessageRepository
from .repositories.memory import InMemoryMessageRepository
from app.services.chat_service import ChatService
from app.services.agent import MockAgent

def get_message_repository(
    db: Session = Depends(get_db),
) -> IMessageRepository:
    backend = os.getenv("REPOSITORY_BACKEND", "sql")
    if backend.lower() == "memory":
        return InMemoryMessageRepository()
    return SQLMessageRepository(db)

def get_chat_service(
    repo: IMessageRepository = Depends(get_message_repository),
) -> ChatService:
    """
    Inyecta ChatService usando repo + MockAgent.
    Más tarde podríamos elegir OpenAIClient según env var.
    """
    return ChatService(repo, agent=MockAgent())