# backend/app/agents/runner.py

import asyncio
import logging
from agents import Runner, RunContextWrapper
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.factory import make_agent

# Silence other libs
for lib in ("openai", "urllib3", "agents", "transitions"):
    logging.getLogger(lib).setLevel(logging.WARNING)

# Our concise logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)


class ConversationRunner:
    """
    FSM runner that logs system prompt + tools + I/O for easy debugging.
    """
    def __init__(self):
        self.runner = Runner()

    def run_step(self, conv: VaccineConversation, user_text: str) -> str:
        # 1) FSM state & payload
        logging.info(f"[FSM] state={conv.state!r}, payload={conv.payload!r}")

        # 2) Agent + instructions
        agent = make_agent(conv.state)
        instr = agent.instructions
        logging.info(f"[Agent] {agent.name}")
        logging.info(f"[Prompt] {instr!r}")

        # 3) Tools available
        tool_names = [tool.name for tool in getattr(agent, "tools", [])]
        logging.info(f"[Tools] {tool_names}")

        # 4) User input
        logging.info(f"[User] {user_text!r}")

        # 5) Run the agent
        coro = self.runner.run(agent, user_text, context=conv)
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(coro)
        finally:
            loop.close()

        # 6) Bot output
        out = getattr(result, "final_output", None) or getattr(result, "output", "")
        text = getattr(out, "text", str(out))
        logging.info(f"[Bot] {text!r}")

        return out