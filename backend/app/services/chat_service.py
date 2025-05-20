# backend/app/services/chat_service.py

from sqlalchemy.orm import Session
from app.repositories.base import ChatNotFoundError, IMessageRepository
from app.models import ConversationState
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.runner import ConversationRunner


class ChatService:
    """
    Business logic for handling user messages and driving a
    FSM-based vaccination‐booking conversation.
    """
    def __init__(self, repo: IMessageRepository):
        self.repo = repo
        self.runner = ConversationRunner()

    def _load_conversation(self, chat_id: int) -> VaccineConversation:
        """
        Fetches or initializes the VaccineConversation FSM for this chat.
        """
        # We expect SQLMessageRepository to expose .db as a Session
        session: Session = self.repo.db  
        state_row = session.query(ConversationState).get(chat_id)
        if not state_row:
            # First time: create new FSM and persist initial state
            conv = VaccineConversation()
            new_state = ConversationState(
                chat_id=chat_id,
                state_name=conv.state,
                payload=conv.payload
            )
            session.add(new_state)
            session.commit()
            return conv

        # Existing conversation: reconstruct FSM
        conv = VaccineConversation(payload=state_row.payload)
        conv.state = state_row.state_name
        return conv

    def _save_conversation(self, chat_id: int, conv: VaccineConversation):
        """
        Persists the updated FSM state & payload back to the DB.
        """
        session: Session = self.repo.db
        state_row = session.query(ConversationState).get(chat_id)
        state_row.state_name = conv.state
        state_row.payload = conv.payload
        session.commit()

    def send_user_message(self, chat_id: int, content: str):
        """
        1. Stores the incoming user message.
        2. Loads (or initializes) the FSM.
        3. Runs one FSM step via the OpenAI-driven runner.
        4. Persists the updated FSM.
        5. Stores and returns the assistant's reply.
        """
        # 1) store user message
        try:
            self.repo.add_message(chat_id, "user", content)
        except ChatNotFoundError:
            # Bubble up as 404 in your router
            raise

        # 2) load or init FSM
        conv = self._load_conversation(chat_id)

        # 3) execute one step of the FSM via the Agent runner
        assistant_text = self.runner.run_step(conv, content)

        # 4) save updated FSM state
        self._save_conversation(chat_id, conv)

        # 5) store assistant message
        assistant_msg = self.repo.add_message(chat_id, "assistant", assistant_text.text)
        return assistant_msg