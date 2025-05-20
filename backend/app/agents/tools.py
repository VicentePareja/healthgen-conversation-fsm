# backend/app/agents/tools.py

from agents import function_tool, RunContextWrapper
from app.fsm.vaccine_fsm import VaccineConversation

@function_tool
def provide_name(
    context: RunContextWrapper[VaccineConversation],
    name: str,
) -> dict:
    """
    Stores the user's name and advances the FSM to the next step.
    ARGUMENTS:
    - name: The user's full name (first and last). Extract this from the user's reply.
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool when you are confident you have extracted the user's name. 
    - If the response is ambiguous, incomplete, or doesn't look like a real name, 
      do NOT call this tool. Instead, rephrase your question and politely ask for their full name.
    - If the user gives a one-word name or a non-name (e.g. "me", "idk"), clarify and prompt for a first and last name.
    - Example good calls: "Alice Smith", "Juan Pérez", "Mary Jane Watson"
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
    Stores the user's age (in years).
    ARGUMENTS:
    - age: An integer from 0 to 120, extracted from the user's reply.
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool if the user's input clearly specifies a valid age as a number (numerals or words, e.g. "22" or "twenty-two").
    - If the user's response cannot be interpreted as a valid age (e.g., "old", "a little", "?", "twenty something"), do NOT call this tool.
    - Instead, politely ask them to reply with their age as a number in years, giving a concrete example (e.g., "Please reply with your age in years, like 36").
    - If the age is out of bounds (below 0 or above 120), do NOT call this tool; prompt again.
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
    Records the user's answer about egg allergy and advances the FSM accordingly.
    ARGUMENTS:
    - allergy: Must be 'yes' or 'no' (accept synonyms: 'nah', 'nope', 'not really' => no; 'yeah', 'of course', 'sure' => yes).
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool if the user's response clearly indicates "yes" or "no" (accepting synonyms and fuzzy matches).
    - If the user's response is ambiguous, uncertain, or does not resemble "yes" or "no" (e.g., "maybe", "I don't know", "probably not"), do NOT call this tool.
    - Instead, politely rephrase your question and ask the user to answer clearly with "yes" or "no".
    - Examples of valid 'no' inputs: "no", "nah", "nope", "not really", "I don't think so", "n"
    - Examples of valid 'yes' inputs: "yes", "yeah", "of course", "absolutely", "sure", "y"
    - For any other type of input, clarify and ask again.
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
    Lets the user pick an appointment slot from the offered list.
    ARGUMENTS:
    - choice: Integer index (1-based) corresponding to the list of available slots shown to the user.
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool if the user's response is a valid number and matches an available slot.
    - If the input is not a valid integer or is out of range, do NOT call this tool.
    - Instead, politely prompt the user to choose a slot by its number (e.g., "Please reply with a number between 1 and 3").
    - If the user asks for clarification, repeat the list of available slots.
    - Example good input: "2" if slot 2 exists.
    """
    conv: VaccineConversation = context.context
    conv.select_slot(choice=choice)
    return {"selected_slot": conv.payload.get("selected_slot")}


@function_tool
def confirm_selection(
    context: RunContextWrapper[VaccineConversation],
) -> dict:
    """
    Moves the FSM into the confirmation state after the user selects a slot.
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool after the user has picked a valid slot and you are ready to confirm the appointment.
    - If the user seems unsure or asks for another slot, do NOT call this tool; repeat the slot selection step.
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
    Finalizes the booking if the user confirms, or returns to slot selection if not.
    ARGUMENTS:
    - yes: Boolean. True if the user confirms ("yes", "confirm", "okay"), False if not ("no", "change", etc.).
    
    INSTRUCTIONS TO THE AGENT:
    - Only call this tool if the user gives a clear yes or no answer to confirmation (accept synonyms as before).
    - If the user's input is ambiguous or they request a change, do NOT call this tool. Instead, clarify or prompt again.
    - If yes, move to completion and confirm the booking. If no, return to slot selection.
    """
    conv: VaccineConversation = context.context
    if yes:
        conv.finish_yes()
    else:
        conv.finish_no()
    return conv.payload