"""W-series axiom checks — awareness, perception vs. witnessing, the knowledge trinity.

Source: ``AwarenessAxioms.lean`` (W2–W11; W1 is derived from A4 + A11).

These axioms formalize the distinction between dualistic *perception* (an event
produced by a conditioned perceiver, W3/W4) and non-dual *witnessing* (timeless,
W2, the Subject's mode, W1/W11). The knower-known-knowing (*tripuṭī*) collapse in the
Subject (W7/W10) is the formal basis for the knower-trinity construct in the library.
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned, is_subject
from ..report import Violation
from ..sorts import Obj


def check_w2_witnessing_timeless(witness: Obj, witnessing_is_event: bool) -> Violation | None:
    """W2 — witnessing is not a temporal event (it is not a PerceptionEvent).

    Witnessing is the Subject's mode; it produces no event and has no timestamp.
    """
    if witnessing_is_event:
        return Violation(
            axiom_id="W2",
            term="sākṣitva (witnessing)",
            explanation=(
                f"W2: witnessing (Witnesses) is not a temporal event — "
                f"it is not an instance of PerceptionEvent. {witness!r}'s witnessing "
                f"is reported as an event, which would make it temporal and conditioned."
            ),
        )
    return None


def check_w3_perception_generates_event(perceiver: Obj, event_exists: bool) -> Violation | None:
    """W3 — dualistic perception generates a temporal event."""
    if is_conditioned(perceiver) and not event_exists:
        return Violation(
            axiom_id="W3",
            term="pratyakṣa (perception)",
            explanation=(
                f"W3: whenever a conditioned entity perceives (Perceives s o), a "
                f"perception-event occurs at some time. {perceiver!r} perceives but "
                f"no corresponding event is recorded."
            ),
        )
    return None


def check_w4_perceiver_conditioned(perceiver: Obj) -> Violation | None:
    """W4 — any perceiver is Conditioned.

    If something perceives (dualistically, subject-vs-object), it is not the Absolute.
    This is the contrapositive of the witness-centered commitment.
    """
    if is_absolute(perceiver):
        return Violation(
            axiom_id="W4",
            term="pratyakṣa / ahaṃkāra",
            explanation=(
                f"W4: any entity that perceives dualistically is Conditioned "
                f"(∃o. Perceives(s, o) → C(s)). {perceiver!r} is the Absolute — "
                f"the Absolute witnesses but never perceives (A13)."
            ),
        )
    return None


def check_w5_witness_of_other_implies_subject(witness: Obj, other: Obj, is_y: bool) -> Violation | None:
    """W5 — if an entity witnesses something other than itself, it is Y.

    (∃x ≠ w. Witnesses(w, x)) → Y(w).
    """
    if witness is not other and not is_y:
        return Violation(
            axiom_id="W5",
            term="sākṣin",
            explanation=(
                f"W5: whatever witnesses something other than itself is the Subject Y. "
                f"{witness!r} witnesses {other!r} (which is distinct from it), but "
                f"{witness!r} is not classified as Y."
            ),
        )
    return None


def check_w6_perception_requires_distinctness(perceiver: Obj, perceived: Obj) -> Violation | None:
    """W6 — in perception, subject and object are distinct (s ≠ o)."""
    if perceiver is perceived:
        return Violation(
            axiom_id="W6",
            term="pratyakṣa",
            explanation=(
                "W6: dualistic perception requires that the perceiver and the perceived "
                "be distinct objects (Perceives s o → s ≠ o). The same entity cannot "
                "dualistically perceive itself."
            ),
        )
    return None


def check_w7_subject_collapses_trinity(subject: Obj,
                                        knower_is_subject: bool,
                                        known_is_subject: bool,
                                        knowing_is_subject: bool) -> Violation | None:
    """W7 — in the Subject, Knower/Known/Knowing collapse into one (all = Y).

    If any DistinctAspects triple exists and the Subject is involved, all three
    aspects must equal the Subject.
    """
    if is_subject(subject):
        not_collapsed = [
            name for name, v in [
                ("Knower (jñātṛ)", knower_is_subject),
                ("Known (jñeya)", known_is_subject),
                ("Knowing (jñāna)", knowing_is_subject),
            ] if not v
        ]
        if not_collapsed:
            return Violation(
                axiom_id="W7",
                term="tripuṭī-nāśa (collapse of the triad)",
                explanation=(
                    f"W7: in the Subject (Y), the Knower/Known/Knowing are all identical "
                    f"to Y (the tripartite structure dissolves). For {subject!r}, the "
                    f"following are not equal to Y: {', '.join(not_collapsed)}."
                ),
            )
    return None


def check_w9_liberating_knowledge_removes_ignorance(
    jiva: Obj,
    possesses_liberating_knowledge: bool,
    still_has_ignorance: bool,
) -> Violation | None:
    """W9 — possessing liberating knowledge removes a jīva's ignorance of the Absolute.

    Liberating(k) ∧ Jiva(j) ∧ A(a) → (Possesses(j, k) → ¬IgnoranceOf(j, a)).
    """
    if possesses_liberating_knowledge and still_has_ignorance:
        return Violation(
            axiom_id="W9",
            term="mokṣa-jñāna / avidyā-nivṛtti",
            explanation=(
                f"W9: possessing liberating knowledge (vidyā) removes ignorance of the "
                f"Absolute. {jiva!r} possesses liberating knowledge but is still reported "
                f"as having ignorance of the Absolute — a contradiction."
            ),
        )
    return None


def check_w11_witness_of_all_is_absolute(entity: Obj, witnesses_all: bool) -> Violation | None:
    """W11 — whatever witnesses everything is the Absolute.

    (∀x. Witnesses(w, x)) → A(w). The converse of A11.
    """
    if witnesses_all and not is_absolute(entity):
        return Violation(
            axiom_id="W11",
            term="sākṣin / Brahman",
            explanation=(
                f"W11: whatever witnesses every entity is the Absolute "
                f"(∀x. Witnesses(w, x) → A(w)). {entity!r} witnesses everything "
                f"but is not classified as the Absolute."
            ),
        )
    return None
