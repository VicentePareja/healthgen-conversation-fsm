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
        State(name="awaiting_intent"),
        State(name="asked_name"),
        State(name="got_name"),
        State(name="got_age"),
        State(name="awaiting_allergy_response"),
        State(name="eligible"),
        State(name="ineligible"),
        State(name="offered_slots"),
        State(name="awaiting_selection"),
        State(name="confirming"),
        State(name="completed"),
        State(name="abort"),
        State(name="fallback"),
    ]

    def __init__(self, payload: dict | None = None, slot_repo=None):
        self.payload = payload or {}
        self.state = "start"
        self.slot_repo = slot_repo or InMemorySlotRepository()

        # ignore_invalid_triggers lets us call e.g. early_cancel()
        self.machine = Machine(
            model=self,
            states=VaccineConversation.states,
            initial="start",
            send_event=True,
            auto_transitions=False,
            ignore_invalid_triggers=True,
        )

        # ─── Intent ───────────────────────────────────────────────────────────────
        self.machine.add_transition(
            trigger="ask_intent",
            source="start",
            dest="awaiting_intent",
        )
        self.machine.add_transition(
            trigger="affirm_intent",
            source="awaiting_intent",
            dest="asked_name",
        )
        self.machine.add_transition(
            trigger="deny_intent",
            source="awaiting_intent",
            dest="abort",
        )
        self.machine.add_transition(
            trigger="unclear_intent",
            source="awaiting_intent",
            dest="fallback",
        )

        # ─── Name ─────────────────────────────────────────────────────────────────
        self.machine.add_transition(
            trigger="provide_name",
            source="asked_name",            
            dest="got_name",
            before="set_name",
        )
        self.machine.add_transition(
            trigger="invalid_name",
            source="asked_name",
            dest="fallback",
        )

        # ─── Age & Ask Allergy ────────────────────────────────────────────────────
        # after provide_age → got_age
        self.machine.add_transition(
            trigger="provide_age",
            source="got_name",
            dest="got_age",
            before="set_age",
        )

        # then this ask_allergy trigger
        self.machine.add_transition(
            trigger="ask_allergy",
            source="got_age",
            dest="awaiting_allergy_response",
        )
        self.machine.add_transition(
            trigger="invalid_age",
            source="got_age",
            dest="fallback",
        )

        # ─── Allergy Answer ───────────────────────────────────────────────────────
        self.machine.add_transition(
            trigger="answer_allergy",
            source="awaiting_allergy_response",
            dest="ineligible",
            conditions="is_allergic_true",
            before="set_allergy",
        )
        self.machine.add_transition(
            trigger="answer_allergy",
            source="awaiting_allergy_response",
            dest="eligible",
            conditions="is_allergic_false",
            before="set_allergy",
            after="offer_slots",
        )
        self.machine.add_transition(
            trigger="unclear_allergy",
            source="awaiting_allergy_response",
            dest="fallback",
        )

        # ─── Slot Selection ──────────────────────────────────────────────────────
        # (offer_slots itself will call to_offered_slots())
        self.machine.add_transition(
            trigger="select_slot",
            source="offered_slots",
            dest="awaiting_selection",
            conditions="is_valid_slot",
            before="set_selected_slot",
        )
        self.machine.add_transition(
            trigger="select_slot",
            source="offered_slots",
            dest="offered_slots",
            unless="is_valid_slot",
            before="set_selected_slot",
        )
        self.machine.add_transition(
            trigger="invalid_slot",
            source="offered_slots",
            dest="fallback",
        )

        # ─── Confirmation ────────────────────────────────────────────────────────
        self.machine.add_transition(
            trigger="confirm",
            source="awaiting_selection",
            dest="confirming",
        )

        # ─── Finish Booking ───────────────────────────────────────────────────────
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
        self.machine.add_transition(
            trigger="reopen_slots",
            source="confirming",
            dest="offered_slots",
        )

        # ─── Early Cancel & Fallback ──────────────────────────────────────────────
        self.machine.add_transition(
            trigger="early_cancel",
            source="*",
            dest="abort",
        )
        self.machine.add_transition(
            trigger="restart_after_fallback",
            source="fallback",
            dest="start",
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
        slots = self.slot_repo.get_next_slots(days=3, per_day=3)
        self.payload["slots"] = slots
        self.to_offered_slots()

    def set_selected_slot(self, event):
        choice = int(event.kwargs.get("choice"))
        slots = self.payload.get("slots", [])
        if 1 <= choice <= len(slots):
            self.payload["selected_slot"] = slots[choice - 1]
        else:
            self.payload["selected_slot"] = None

    def is_valid_slot(self, event) -> bool:
        try:
            idx = int(event.kwargs.get("choice")) - 1
            slots = self.payload.get("slots", [])
            return 0 <= idx < len(slots)
        except Exception:
            return False