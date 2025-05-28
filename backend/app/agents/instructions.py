# backend/app/agents/instructions.py

from typing import Callable, Dict, Union, Any

def dynamic_confirming(context: Any, agent: Any) -> str:
    """
    Generates the confirmation prompt using the selected slot,
    asking the user to reply with a clear 'yes' or 'no'.
    """
    slot = context.context.payload.get("selected_slot")
    return (
        f"You have selected the appointment at {slot}. "
        "Please confirm by replying 'yes' or 'no'."
    )

def dynamic_completion(context: Any, agent: Any) -> str:
    """
    Final confirmation message once booking is done.
    """
    slot = context.context.payload.get("selected_slot")
    return f"Your appointment is confirmed at {slot}. Thank you!"

def dynamic_offer_slots(context: Any, agent: Any) -> str:
    """
    Enumerate context.context.payload['slots'] and prompt for a numeric choice.
    """
    slots = context.context.payload.get("slots", [])
    if not slots:
        return "I’m sorry, no slots are available right now."
    lines = [f"{i+1}) {slot}" for i, slot in enumerate(slots)]
    return (
        "Here are the available appointment slots:\n\n"
        + "\n".join(lines)
        + f"\n\nPlease choose a slot by its number (1–{len(slots)}). "
          "Only respond with the number; if it’s invalid, I will show these again."
    )

STATE_INSTRUCTIONS: Dict[str, Union[str, Callable[..., str]]] = {
    "start": (
        "You are a friendly assistant. Ask the user for their full name (first and last). "
        "Only call the provide_name tool when you are confident you have extracted both first and last name. "
        "If the response is ambiguous or incomplete, rephrase your question: "
        "'Could you please tell me your full name, including first and last name?'"
    ),

    "got_name": (
        "You are a friendly assistant. Thank you! Now ask the user: 'How old are you?' "
        "You must only call the provide_age tool if the response is a valid integer between 0 and 120. "
        "If the user's input is not clearly a number or is out of range, do NOT call the tool. "
        "Instead, say: 'Please reply with your age in years, for example: 36.'"
    ),

    "got_age": (
        "You are a friendly assistant. Great. Next, ask the user: 'Do you have any known egg allergy?' "
        "Require a clear 'yes' or 'no' answer. "
        "Only call the answer_allergy tool if the response clearly maps to yes/no (accept synonyms like 'nah', 'nope', 'absolutely'). "
        "If the answer is ambiguous (e.g. 'maybe', 'I’m not sure'), rephrase and ask: "
        "'Please answer with yes or no: do you have an egg allergy?'"
    ),

    "asked_allergy": (
        "You are a friendly assistant. Repeat if needed: 'Do you have any known egg allergy? Please reply yes or no.' "
        "Only call the answer_allergy tool on a clear yes/no. "
        "Otherwise, re-prompt."
    ),

    "eligible": (
        "You are a friendly assistant. The user is eligible. You have in context.payload['slots'] a list of ISO datetimes. "
        "Enumerate them as '1) 2025-05-20T09:00', '2) 2025-05-20T11:00', etc., then ask: "
        "'Please choose a slot by its number.' "
        "Only call the select_slot tool when the user replies with a valid integer matching one of the options. "
        "If the input is not a valid option, say: 'Please choose a number between 1 and {len(context.context.payload['slots'])}.'"
    ),

    "offered_slots": dynamic_offer_slots,

    "awaiting_selection": (
        "You are a friendly assistant. The user has picked a slot number. Call the confirm_selection tool now. "
        "If they express uncertainty or ask to change, rephrase: "
        "'Would you like to change your selection? Please reply yes to confirm or no to choose again.'"
    ),

    "confirming": dynamic_confirming,

    "ineligible": (
        "Politely inform the user they are not eligible for the influenza vaccine and end the conversation. "
        "For example: 'I’m sorry, based on the information provided you are not eligible for this vaccine.'"
    ),

    "completed": dynamic_completion,
}