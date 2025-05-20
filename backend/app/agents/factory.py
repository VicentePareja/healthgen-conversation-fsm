# backend/app/agents/factory.py

from agents import Agent
from app.schemas import ConversationReply
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.tools import (
    provide_name,
    provide_age,
    answer_allergy,
    select_slot,
    confirm_selection,
    finish_booking,
)
from app.agents.config import MODEL_NAME, DEFAULT_MODEL_SETTINGS
from app.agents.instructions import STATE_INSTRUCTIONS

# Map each state to its allowed tools
TOOLS_MAP: dict[str, list] = {
    "start": [provide_name],
    "got_name": [provide_age],
    "got_age": [answer_allergy],
    "asked_allergy": [answer_allergy],
    "eligible": [select_slot],
    "offered_slots": [select_slot],
    "awaiting_selection": [confirm_selection],
    "confirming": [finish_booking],
    "ineligible": [],
    "completed": [],
}

def make_agent(state: str) -> Agent[VaccineConversation]:
    instr = STATE_INSTRUCTIONS.get(state)
    tools = TOOLS_MAP.get(state, [])
    # All outputs are ConversationReply (strict Pydantic)
    output_type = ConversationReply

    return Agent[VaccineConversation](
        name=f"{state.capitalize()}Agent",
        instructions=instr,
        model=MODEL_NAME,
        model_settings=DEFAULT_MODEL_SETTINGS,
        tools=tools,
        output_type=output_type,
    )