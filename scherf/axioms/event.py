"""E-series axiom checks — events and causation.

Source: ``EventAxioms.lean`` (E1–E10) and CA1/CA4 from ``AdditionalAxioms.lean``.

Key principle: the Absolute has no events (E10) and no temporal properties (A7a).
All events occur at the *vyāvahārika* level (CA1). Perception events arise only
from conditioned perceivers (W3/W4).
"""

from __future__ import annotations

from ..ontology import is_absolute
from ..report import Violation
from ..sorts import Obj


def check_e1_event_exists_iff_occurs(event_id: str,
                                      has_occurrence_time: bool,
                                      claimed_to_exist: bool) -> Violation | None:
    """E1 — EE(e) ↔ ∃t. OccursAt(e, t): event exists iff it occurs at some time."""
    if claimed_to_exist and not has_occurrence_time:
        return Violation(
            axiom_id="E1",
            term="kārya (event existence)",
            explanation=(
                f"E1: an event exists (EE e) iff it occurs at some time "
                f"(∃t. OccursAt e t). Event {event_id!r} is claimed to exist "
                f"but has no occurrence time."
            ),
        )
    if has_occurrence_time and not claimed_to_exist:
        return Violation(
            axiom_id="E1",
            term="kārya (event existence)",
            explanation=(
                f"E1: an event that occurs at a time must exist. Event {event_id!r} "
                f"has an occurrence time but is not claimed to exist."
            ),
        )
    return None


def check_e2_unique_occurrence(event_id: str, occurrence_count: int) -> Violation | None:
    """E2 — an existing event occurs at exactly one time instant."""
    if occurrence_count > 1:
        return Violation(
            axiom_id="E2",
            term="kārya (unique occurrence)",
            explanation=(
                f"E2: an existing event occurs at a unique time instant. "
                f"Event {event_id!r} has {occurrence_count} occurrence times."
            ),
        )
    return None


def check_e9_causal_ordering(cause_time: object, effect_time: object,
                               cause_before_effect: bool) -> Violation | None:
    """E9 — causation implies temporal precedence: CausesEvent e1 e2 → Before t1 t2."""
    if not cause_before_effect:
        return Violation(
            axiom_id="E9",
            term="kāraṇa-kārya (causal ordering)",
            explanation=(
                f"E9: if e1 causes e2 then e1 must occur before e2. "
                f"Cause time {cause_time!r} is not before effect time {effect_time!r}."
            ),
        )
    return None


def check_e10_absolute_no_events(x: Obj, has_events: bool) -> Violation | None:
    """E10 — the Absolute has no events (A a → ¬EventOf e a for any e)."""
    if is_absolute(x) and has_events:
        return Violation(
            axiom_id="E10",
            term="nirvikāra (eventless Absolute)",
            explanation=(
                f"E10: the Absolute has no events — no event is associated with it "
                f"(∀e. A a → ¬EventOf e a). {x!r} is the Absolute but has events "
                f"associated with it."
            ),
        )
    return None
