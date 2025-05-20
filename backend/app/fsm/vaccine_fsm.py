# backend/app/fsm/vaccine_fsm.py

from transitions import Machine, State
from datetime import datetime, timedelta
from app.repositories.memory import InMemorySlotRepository


class VaccineConversation:
    """
    FSM for guiding a user through scheduling an influenza vaccination.
    Payload holds: name, age, allergy (bool), slots (list of str), selected_slot.
    """

    states = [
        State(name="start"),
        State(name="got_name"),
        State(name="got_age"),
        State(name="asked_allergy"),
        State(name="eligible"),
        State(name="ineligible"),
        State(name="offered_slots"),
        State(name="awaiting_selection"),
        State(name="confirming"),
        State(name="completed"),
    ]

    def __init__(self, payload: dict | None = None, slot_repo=None):
        # persistent data across the flow
        self.payload = payload or {}
        # initial state
        self.state = "start"

        self.slot_repo = slot_repo or InMemorySlotRepository()

        # build the state machine
        self.machine = Machine(
            model=self,
            states=VaccineConversation.states,
            initial="start",
            send_event=True,
            auto_transitions=False,
        )

        # transitions
        self.machine.add_transition(
            trigger="provide_name",
            source="start",
            dest="got_name",
            before="set_name",
        )
        self.machine.add_transition(
            trigger="provide_age",
            source="got_name",
            dest="got_age",
            before="set_age",
            after="ask_allergy",            # immediately ask allergy after age
        )
        self.machine.add_transition(
            trigger="answer_allergy",
            source="asked_allergy",
            dest="ineligible",
            conditions="is_allergic_true",
            before="set_allergy",
        )
        self.machine.add_transition(
            trigger="answer_allergy",
            source="asked_allergy",
            dest="eligible",
            conditions="is_allergic_false",
            before="set_allergy",
            after="offer_slots",           # eligible → go offer slots
        )
        self.machine.add_transition(
            trigger="select_slot",
            source="offered_slots",
            dest="awaiting_selection",
            before="set_selected_slot",
        )
        self.machine.add_transition(
            trigger="confirm",
            source="awaiting_selection",
            dest="confirming",
        )
        self.machine.add_transition(
            trigger="finish_yes",
            source="confirming",
            dest="completed",
        )
        self.machine.add_transition(
            trigger="finish_no",
            source="confirming",
            dest="offered_slots",
        )

    # ─── CALLBACKS & CONDITIONS ─────────────────────────────────────────────────

    def set_name(self, event):
        name = event.kwargs.get("name", "").strip()
        self.payload["name"] = name

    def set_age(self, event):
        age = event.kwargs.get("age")
        # normalize to int
        self.payload["age"] = int(age)

    def ask_allergy(self, event):
        # transition into asked_allergy
        self.to_asked_allergy()

    def set_allergy(self, event):
        answer = event.kwargs.get("allergy")
        # normalize yes/no
        self.payload["allergy"] = str(answer).lower() in ["yes", "y", "true"]

    def is_allergic_true(self, event) -> bool:
        return str(event.kwargs.get("allergy")).lower() in ["yes", "y", "true"]

    def is_allergic_false(self, event) -> bool:
        return str(event.kwargs.get("allergy")).lower() in ["no", "n", "false"]

    def offer_slots(self, event):
        # generate next 3 days × 3 times
        slots = self.slot_repo.get_next_slots(days=3, per_day=3)
        self.payload["slots"] = slots
        # move to offered_slots state
        self.to_offered_slots()

    def set_selected_slot(self, event):
        choice = event.kwargs.get("choice")
        idx = int(choice) - 1
        slots = self.payload.get("slots", [])
        if 0 <= idx < len(slots):
            self.payload["selected_slot"] = slots[idx]
        else:
            # invalid choice; leave payload untouched
            self.payload["selected_slot"] = None