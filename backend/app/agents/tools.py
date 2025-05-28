# backend/app/agents/tools.py

from agents import function_tool, RunContextWrapper
from app.fsm.vaccine_fsm import VaccineConversation

# ─── Intent ───────────────────────────────────────────────────────────────────

@function_tool
def ask_intent(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    After greeting, ask the user whether they want to schedule a vaccination.
    """
    conv: VaccineConversation = context.context
    conv.ask_intent()
    return conv.payload

@function_tool
def affirm_intent(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    User said 'yes' to scheduling.
    """
    conv: VaccineConversation = context.context
    conv.affirm_intent()
    return conv.payload

@function_tool
def deny_intent(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    User said 'no' to scheduling.
    """
    conv: VaccineConversation = context.context
    conv.deny_intent()
    return conv.payload

@function_tool
def unclear_intent(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    User response was not a clear yes/no.
    """
    conv: VaccineConversation = context.context
    conv.unclear_intent()
    return conv.payload


# ─── Name ─────────────────────────────────────────────────────────────────────

@function_tool
def provide_name(
    context: RunContextWrapper[VaccineConversation],
    name: str,
) -> dict:
    """
    Stores the user's full name.
    """
    conv: VaccineConversation = context.context
    conv.provide_name(name=name)
    return conv.payload

@function_tool
def invalid_name(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Name not recognised; trigger fallback.
    """
    conv: VaccineConversation = context.context
    conv.invalid_name()
    return conv.payload


# ─── Age ───────────────────────────────────────────────────────────────────────

@function_tool
def provide_age(
    context: RunContextWrapper[VaccineConversation],
    age: int,
) -> dict:
    """
    Stores the user's age.
    """
    conv: VaccineConversation = context.context
    conv.provide_age(age=age)
    return conv.payload

@function_tool
def invalid_age(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Age input invalid; trigger fallback.
    """
    conv: VaccineConversation = context.context
    conv.invalid_age()
    return conv.payload


# ─── Allergy ───────────────────────────────────────────────────────────────────

@function_tool
def answer_allergy(
    context: RunContextWrapper[VaccineConversation],
    allergy: str,
) -> dict:
    """
    Records egg‐allergy yes/no.
    """
    conv: VaccineConversation = context.context
    conv.answer_allergy(allergy=allergy)
    return conv.payload

@function_tool
def unclear_allergy(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Allergy answer ambiguous; trigger fallback.
    """
    conv: VaccineConversation = context.context
    conv.unclear_allergy()
    return conv.payload


# ─── Slot Selection ────────────────────────────────────────────────────────────

@function_tool
def select_slot(
    context: RunContextWrapper[VaccineConversation],
    choice: int,
) -> dict:
    """
    User picks one of the offered slots.
    """
    conv: VaccineConversation = context.context
    conv.select_slot(choice=choice)
    return {"selected_slot": conv.payload.get("selected_slot")}

@function_tool
def invalid_slot(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Slot choice invalid; trigger fallback.
    """
    conv: VaccineConversation = context.context
    conv.invalid_slot()
    return conv.payload


# ─── Confirmation ─────────────────────────────────────────────────────────────

@function_tool
def confirm_selection(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Move into the confirming state.
    """
    conv: VaccineConversation = context.context
    conv.confirm()
    return conv.payload


# ─── Finish Booking ────────────────────────────────────────────────────────────

@function_tool
def finish_booking(
    context: RunContextWrapper[VaccineConversation],
    yes: bool,
) -> dict:
    """
    Finalize or reopen slots based on yes/no.
    """
    conv: VaccineConversation = context.context
    if yes:
        conv.finish_yes()
    else:
        conv.finish_no()
    return conv.payload


# ─── Global Cancels & Fallback ─────────────────────────────────────────────────

@function_tool
def early_cancel(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    User cancels at any point.
    """
    conv: VaccineConversation = context.context
    conv.early_cancel()
    return conv.payload

@function_tool
def restart_after_fallback(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    After a fallback reprompt, restart the flow (or hook in prev‐state logic later).
    """
    conv: VaccineConversation = context.context
    conv.restart_after_fallback()
    return conv.payload