# backend/app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas import Chat as ChatSchema, Message as MessageSchema, MessageCreate
from app.repositories.base import ChatNotFoundError
from app.dependencies import get_message_repository, get_chat_service
from app.repositories.base import IMessageRepository
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ChatSchema, status_code=status.HTTP_201_CREATED)
def create_chat(repo: IMessageRepository = Depends(get_message_repository)):
    """
    Create a new chat and return its metadata.
    """
    return repo.create_chat()


@router.get("/", response_model=List[ChatSchema])
def list_chats(repo: IMessageRepository = Depends(get_message_repository)):
    """
    List all existing chats.
    """
    return repo.list_chats()


@router.post(
    "/{chat_id}/messages",
    response_model=MessageSchema,
    status_code=status.HTTP_201_CREATED,
)
def post_message(
    chat_id: int,
    message_in: MessageCreate,
    service: ChatService = Depends(get_chat_service),
):
    """
    Send a user message to a chat and receive the bot response.
    """
    try:
        return service.send_user_message(chat_id, message_in.content)
    except ChatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id={chat_id} not found",
        )


@router.get(
    "/{chat_id}/messages",
    response_model=List[MessageSchema],
)
def get_messages(
    chat_id: int,
    repo: IMessageRepository = Depends(get_message_repository),
):
    """
    Retrieve all messages for a given chat.
    """
    try:
        return repo.get_messages(chat_id)
    except ChatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id={chat_id} not found",
        )