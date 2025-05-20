# backend/app/agents/instructions.py

from typing import Callable, Dict, Union, Any

def dynamic_confirming(context: Any, agent: Any) -> str:
    """
    Generates the confirmation prompt using the selected slot.
    """
    slot = context.context.payload.get("selected_slot")
    return f"Please confirm your appointment at {slot}. Reply yes or no."

def dynamic_completion(context: Any, agent: Any) -> str:
    """
    Final confirmation message once booking is done.
    """
    slot = context.context.payload.get("selected_slot")
    return f"Your appointment is confirmed at {slot}. Thank you!"

STATE_INSTRUCTIONS: Dict[str, Union[str, Callable[..., str]]] = {
    "start": (
        "You are a friendly assistant. Ask the user for their full name (first and last)."
    ),
    "got_name": (
        "Thank you! Now ask the user: 'How old are you?' "
        "Please respond with a number (in years)."
    ),
    "got_age": (
        "Ask the user if they have any known egg allergy. "
        "Please respond 'yes' or 'no'."
    ),
    "asked_allergy": (
        "Ask the user if they have any known egg allergy. "
        "Please respond 'yes' or 'no'."
    ),
    "eligible": (
        "You have a list of available slots in context.payload['slots'], "
        "enumerate them like '1) 2025-05-20T09:00', etc., "
        "and ask: 'Please choose a slot by its number.'"
    ),
    "offered_slots": (
        "You have a list of available slots in context.payload['slots'], "
        "enumerate them like '1) 2025-05-20T09:00', etc., "
        "and ask: 'Please choose a slot by its number.'"
    ),
    "awaiting_selection": (
        "The user has picked a slot. Call the 'confirm_selection' tool to move into confirmation."
    ),
    "confirming": dynamic_confirming,
    "ineligible": (
    "Politely inform the user they are not eligible for the influenza vaccine and end the conversation. "
    ),
    "completed": dynamic_completion,
}