# backend/app/agents/tools.py
import logging
from functools import wraps
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
    logging.info("[Tool] ask_intent called")
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
    logging.info("[Tool] affirm_intent called")
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
    logging.info("[Tool] deny_intent called")
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
    logging.info("[Tool] unclear_intent called")
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
    logging.info("[Tool] provide_name called")
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
    logging.info("[Tool] invalid_name called")
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
    logging.info("[Tool] provide_age called")
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
    logging.info("[Tool] invalid_age called")
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
    logging.info("[Tool] answer_allergy called")
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
    logging.info("[Tool] unclear_allergy called")
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
    logging.info(f"[Tool] select_slot called with choice={choice}")
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
    logging.info("[Tool] invalid_slot called")
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
    logging.info("[Tool] confirm_selection called")
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
    logging.info(f"[Tool] finish_booking called with yes={yes}")
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
    logging.info("[Tool] early_cancel called")
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
    logging.info("[Tool] restart_after_fallback called")
    conv: VaccineConversation = context.context
    conv.restart_after_fallback()
    return conv.payload

@function_tool
def ask_allergy(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    After we have the age, ask the user about egg allergy.
    """
    logging.info("[Tool] ask_allergy called")
    conv: VaccineConversation = context.context
    conv.ask_allergy()
    return conv.payload