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
        self.payload = payload or {}
        self.state = "start"
        self.slot_repo = slot_repo or InMemorySlotRepository()

        self.machine = Machine(
            model=self,
            states=VaccineConversation.states,
            initial="start",
            send_event=True,
            auto_transitions=False,
        )

        # 1) Name → got_name
        self.machine.add_transition(
            trigger="provide_name",
            source="start",
            dest="got_name",
            before="set_name",
        )

        # 2) Age → got_age, then fire ask_allergy trigger
        self.machine.add_transition(
            trigger="provide_age",
            source="got_name",
            dest="got_age",
            before="set_age",
            after="ask_allergy",      # this is the *trigger* we're about to define
        )

        # 3) Proper trigger to move from got_age → asked_allergy
        self.machine.add_transition(
            trigger="ask_allergy",
            source="got_age",
            dest="asked_allergy",
        )

        # 4) Allergy answer → ineligible or eligible
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
            after="offer_slots",      # now we move to offered_slots
        )

        # 5) Slot selection → awaiting_selection
        self.machine.add_transition(
            trigger="select_slot",
            source="offered_slots",
            dest="awaiting_selection",
            before="set_selected_slot",
        )

        # 6) Confirm choice → confirming
        self.machine.add_transition(
            trigger="confirm",
            source="awaiting_selection",
            dest="confirming",
        )

        # 7) Finish booking → completed or back to offered_slots
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
        self.payload["name"] = event.kwargs.get("name", "").strip()

    def set_age(self, event):
        self.payload["age"] = int(event.kwargs.get("age"))

    def set_allergy(self, event):
        answer = event.kwargs.get("allergy")
        self.payload["allergy"] = str(answer).lower() in ["yes", "y", "true"]

    def is_allergic_true(self, event) -> bool:
        return str(event.kwargs.get("allergy")).lower() in ["yes", "y", "true"]

    def is_allergic_false(self, event) -> bool:
        return str(event.kwargs.get("allergy")).lower() in ["no", "n", "false"]

    def offer_slots(self, event):
        # fetch next 3 days × 3 slots/day
        slots = self.slot_repo.get_next_slots(days=3, per_day=3)
        self.payload["slots"] = slots
        # transition into offered_slots
        self.to_offered_slots()

    def set_selected_slot(self, event):
        choice = int(event.kwargs.get("choice"))
        slots = self.payload.get("slots", [])
        if 1 <= choice <= len(slots):
            self.payload["selected_slot"] = slots[choice - 1]
        else:
            self.payload["selected_slot"] = None