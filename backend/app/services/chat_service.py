from sqlalchemy.orm import Session
from app.repositories.base import ChatNotFoundError, IMessageRepository
from app.models import ConversationState
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.runner import ConversationRunner

class ChatService:
    def __init__(self, repo: IMessageRepository):
        self.repo = repo
        self.runner = ConversationRunner(repo)

    def _load_conversation(self, chat_id: int) -> VaccineConversation:
        session: Session = self.repo.db
        state_row = session.query(ConversationState).get(chat_id)
        if not state_row:
            conv = VaccineConversation()
            session.add(
                ConversationState(
                    chat_id=chat_id,
                    state_name=conv.state,
                    payload=conv.payload,
                )
            )
            session.commit()
            return conv

        conv = VaccineConversation(payload=state_row.payload)
        conv.state = state_row.state_name
        return conv

    def _save_conversation(self, chat_id: int, conv: VaccineConversation):
        session: Session = self.repo.db
        state_row = session.query(ConversationState).get(chat_id)

        state_row.state_name = conv.state

        state_row.payload    = conv.payload

        state_row.name          = conv.payload.get("name")
        state_row.age           = conv.payload.get("age")
        state_row.allergy       = conv.payload.get("allergy")
        state_row.selected_slot = conv.payload.get("selected_slot")

        session.commit()

    def send_user_message(self, chat_id: int, content: str):
        try:
            self.repo.add_message(chat_id, "user", content)
        except ChatNotFoundError:
            raise

        conv = self._load_conversation(chat_id)
        raw_history = self.repo.get_messages(chat_id)
        history = [{"role": m.role, "content": m.content} for m in raw_history]
        assistant_text = self.runner.run_step(conv, content, history)
        self._save_conversation(chat_id, conv)
        return self.repo.add_message(chat_id, "assistant", assistant_text.text)