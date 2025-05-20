# backend/app/agents/runner.py

import asyncio
from agents import Runner
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.factory import make_agent

class ConversationRunner:
    """
    Orchestrates one step of the VaccineConversation FSM
    using the agents framework.
    """
    def __init__(self):
        self.runner = Runner()

    def run_step(self, conv: VaccineConversation, user_text: str) -> str:
        """
        Given an existing VaccineConversation (with state & payload loaded)
        and the latest user_text, run the appropriate Agent and return
        the assistant’s reply.
        """
        # pick the right agent
        agent = make_agent(conv.state)

        # build the coroutine
        coro = self.runner.run(agent, user_text, context=conv)

        # create a fresh loop for this thread
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(coro)
        finally:
            loop.close()

        # return the final output
        return result.final_output