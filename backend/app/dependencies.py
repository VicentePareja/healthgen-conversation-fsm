# backend/app/dependencies.py

import os
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .repositories.base import IMessageRepository, ChatNotFoundError
from .repositories.sql import SQLMessageRepository
from .repositories.memory import InMemoryMessageRepository

from app.services.chat_service import ChatService
from app.services.agent import MockAgent, OpenAIAgent


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
    Inyecta ChatService con MockAgent o OpenAIAgent,
    según la variable USE_MOCK_AGENT.
    """
    use_mock = os.getenv("USE_MOCK_AGENT", "true").lower() in ["1", "true", "yes"]
    if use_mock:
        agent = MockAgent()
    else:
        try:
            agent = OpenAIAgent()
        except ValueError as e:
            # Si falta la clave, devolvemos 500
            raise HTTPException(status_code=500, detail=str(e))
    return ChatService(repo, agent=agent)