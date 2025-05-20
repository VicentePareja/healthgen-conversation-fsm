# backend/app/agents/tools.py

from agents import function_tool, RunContextWrapper
from app.fsm.vaccine_fsm import VaccineConversation

@function_tool
def provide_name(
    context: RunContextWrapper[VaccineConversation],
    name: str,
) -> dict:
    """
    Store the user’s name and advance FSM to got_name.
    """
    conv: VaccineConversation = context.context
    conv.provide_name(name=name)
    return conv.payload


@function_tool
def provide_age(
    context: RunContextWrapper[VaccineConversation],
    age: int,
) -> dict:
    """
    Store the user’s age and advance FSM to got_age → asked_allergy.
    """
    conv: VaccineConversation = context.context
    conv.provide_age(age=age)
    return conv.payload


@function_tool
def answer_allergy(
    context: RunContextWrapper[VaccineConversation],
    allergy: str,
) -> dict:
    """
    Record allergy response and branch to eligible or ineligible.
    """
    conv: VaccineConversation = context.context
    conv.answer_allergy(allergy=allergy)
    return conv.payload


@function_tool
def select_slot(
    context: RunContextWrapper[VaccineConversation],
    choice: int,
) -> dict:
    """
    Let user pick a slot (1-based index). Moves FSM to awaiting_selection.
    """
    conv: VaccineConversation = context.context
    conv.select_slot(choice=choice)
    return {"selected_slot": conv.payload.get("selected_slot")}


@function_tool
def confirm_selection(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Move FSM into confirming state (will prompt for yes/no).
    """
    conv: VaccineConversation = context.context
    conv.confirm()
    return conv.payload


@function_tool
def finish_booking(
    context: RunContextWrapper[VaccineConversation],
    yes: bool,
) -> dict:
    """
    Finalize or loop back: yes→completed, no→offered_slots.
    Returns full payload when done.
    """
    conv: VaccineConversation = context.context
    if yes:
        conv.finish_yes()
    else:
        conv.finish_no()
    return conv.payload