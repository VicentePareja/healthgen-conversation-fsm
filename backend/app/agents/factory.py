# backend/app/agents/factory.py

from agents import Agent
from app.schemas import ConversationReply
from app.fsm.vaccine_fsm import VaccineConversation
from app.agents.tools import (
    ask_intent,
    affirm_intent,
    deny_intent,
    unclear_intent,
    provide_name,
    invalid_name,
    provide_age,
    invalid_age,
    ask_allergy,
    answer_allergy,
    unclear_allergy,
    select_slot,
    invalid_slot,
    confirm_selection,
    finish_booking,
    early_cancel,
    restart_after_fallback,
)
from app.agents.config import MODEL_NAME, DEFAULT_MODEL_SETTINGS
from app.agents.instructions import STATE_INSTRUCTIONS

TOOLS_MAP: dict[str, list] = {
    "start":              [ask_intent],
    "awaiting_intent":    [affirm_intent, deny_intent, unclear_intent],
    "asked_name":         [provide_name, invalid_name],
    "got_name":           [provide_age, invalid_age],
    "got_age":            [ask_allergy],                   
    "awaiting_allergy_response": [answer_allergy, unclear_allergy],
    "eligible":           [select_slot],
    "offered_slots":      [select_slot, invalid_slot],
    "awaiting_selection": [confirm_selection],
    "confirming":         [finish_booking, early_cancel],
    "ineligible":         [early_cancel],
    "completed":          [],
    "abort":              [],
    "fallback":           [restart_after_fallback],
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