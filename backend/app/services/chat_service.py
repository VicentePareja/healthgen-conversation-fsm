# backend/app/services/chat_service.py

from app.repositories.base import ChatNotFoundError, IMessageRepository
from app.services.agent import MockAgent

class ChatService:
    """
    Lógica de negocio para enviar mensajes de usuario al bot y guardar la respuesta.
    """
    def __init__(self, repo: IMessageRepository, agent=None):
        self.repo = repo
        self.agent = agent or MockAgent()

    def send_user_message(self, chat_id: int, content: str):
        try:
            self.repo.add_message(chat_id, "user", content)
        except ChatNotFoundError as e:
            raise

        history = [
            {"role": m.role, "content": m.content}
            for m in self.repo.get_messages(chat_id)
        ]

        response_text = self.agent.get_response(history)

        assistant_msg = self.repo.add_message(chat_id, "assistant", response_text)
        return assistant_msg