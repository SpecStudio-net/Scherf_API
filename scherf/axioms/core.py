"""A-series and CH-series axiom checks.

Source: ``CoreAxioms.lean`` (A1–A14) and the CH-series in ``AdditionalAxioms.lean``
(CH1–CH4). These establish the fundamental partition of entities into Absolute/
Conditioned, the identity of Subject and Absolute (*Tat Tvam Asi*), and the
permanence/change properties of each.

Most A-series axioms are enforced *structurally* by :mod:`scherf.ontology` and are
documented here as explicit no-ops. Violations that *can* arise at the claim level
(A13, A14) return ``Violation`` instances for the engine to report.
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned, is_subject
from ..report import Violation
from ..sorts import Obj


# --- A1: Exhaustive exclusive partition (A1a / A1b) ----------------------------
# Enforced structurally: Obj is abstract; every entity is Subject XOR Conditioned.

def check_a1(x: Obj) -> Violation | None:
    """A1 (A1a/A1b) — every entity is Absolute or Conditioned, not both, not neither.

    Structurally guaranteed by the type system; always returns ``None``.
    Provided for explicit coverage and testing.
    """
    a, c = is_absolute(x), is_conditioned(x)
    if a and c:
        return Violation(
            axiom_id="A1b",
            term="sat / asat",
            explanation=f"{x!r} is classified as both Absolute and Conditioned — impossible by A1b.",
        )
    if not a and not c:
        return Violation(
            axiom_id="A1a",
            term="sat / asat",
            explanation=f"{x!r} is neither Absolute nor Conditioned — impossible by A1a.",
        )
    return None


# --- A2: Unique Absolute -------------------------------------------------------
# Enforced structurally: Subject.__new__ prevents a second instance.

def check_a2_uniqueness(candidate_absolute: Obj, known_absolute: Obj) -> Violation | None:
    """A2 — there is exactly one Absolute.

    If two distinct objects are both classified Absolute, A2 is violated.
    """
    if candidate_absolute is not known_absolute and is_absolute(candidate_absolute):
        return Violation(
            axiom_id="A2",
            term="Brahman",
            explanation=(
                f"A2: there is exactly one Absolute. {candidate_absolute!r} and "
                f"{known_absolute!r} are both classified Absolute — impossible."
            ),
        )
    return None


# --- A3: Unique Subject --------------------------------------------------------
# Enforced structurally alongside A2 (same singleton).

def check_a3_uniqueness(candidate_subject: Obj, known_subject: Obj) -> Violation | None:
    """A3 — there is exactly one Subject (Y)."""
    if candidate_subject is not known_subject and is_subject(candidate_subject):
        return Violation(
            axiom_id="A3",
            term="sākṣin / Ātman",
            explanation=(
                f"A3: exactly one Subject. {candidate_subject!r} and "
                f"{known_subject!r} are both classified Y — impossible."
            ),
        )
    return None


# --- A4: Tat Tvam Asi (Y ↔ A) -------------------------------------------------

def check_a4(x: Obj) -> Violation | None:
    """A4 (*Tat Tvam Asi*) — the Subject is the Absolute and vice versa (Y ↔ A).

    Any object classified as Subject but not Absolute, or Absolute but not Subject,
    violates A4.
    """
    y, a = is_subject(x), is_absolute(x)
    if y != a:
        which = "Subject (Y) but not Absolute" if y else "Absolute but not Subject (Y)"
        return Violation(
            axiom_id="A4",
            term="Tat Tvam Asi",
            explanation=(
                f"A4: Y ↔ A. {x!r} is {which}. The Subject and the Absolute are "
                f"identical — they cannot come apart."
            ),
        )
    return None


# --- A6: Universal grounding ---------------------------------------------------

def check_a6_grounded(x: Obj, grounded_in_absolute: bool) -> Violation | None:
    """A6 — everything is grounded in some Absolute.

    ``grounded_in_absolute`` should be ``True`` if the caller has confirmed that
    there exists an Absolute ``a`` such that ``Cond(a, x)`` holds.
    """
    if not grounded_in_absolute:
        return Violation(
            axiom_id="A6",
            term="ādhāra",
            explanation=(
                f"A6: every entity is grounded in the Absolute (∃a. A(a) ∧ Cond(a, x)). "
                f"{x!r} has no such grounding."
            ),
        )
    return None


# --- A8: Conditioned is phenomenal (has T_p ∨ S_p ∨ Q_p) ----------------------

def check_a8(x: Obj, is_phenomenal: bool) -> Violation | None:
    """A8 — a Conditioned entity possesses phenomenal properties (Φ).

    ``is_phenomenal`` should be ``True`` if the entity has at least one of
    temporal, spatial, or qualitative properties.
    """
    if is_conditioned(x) and not is_phenomenal:
        return Violation(
            axiom_id="A8",
            term="Phi (T_p ∨ S_p ∨ Q_p)",
            explanation=(
                f"A8: every Conditioned entity possesses phenomenal properties "
                f"(temporal, spatial, or qualitative). {x!r} is Conditioned but "
                f"has none."
            ),
        )
    return None


# --- A11: Absolute witnesses everything ----------------------------------------

def check_a11(x: Obj, witnesses_all: bool) -> Violation | None:
    """A11 — the Absolute witnesses every entity.

    ``witnesses_all`` should be ``True`` if ``Witnesses(x, ·)`` holds for all
    entities. Called to verify the Absolute's witnessing is complete.
    """
    if is_absolute(x) and not witnesses_all:
        return Violation(
            axiom_id="A11",
            term="sākṣitva",
            explanation=(
                f"A11: the Absolute witnesses everything. {x!r} is the Absolute but "
                f"its witnessing is reported as incomplete."
            ),
        )
    return None


# --- A13: Subject never perceives dualistically --------------------------------

def check_a13(claimed_perceiver: Obj, claimed_object: Obj) -> Violation | None:
    """A13 — the Subject (Y) never perceives dualistically.

    If the claimed perceiver is the Subject, this is a violation: dualistic
    perception (subject-vs-object) is a property of conditioned perceivers only.
    """
    if is_subject(claimed_perceiver):
        return Violation(
            axiom_id="A13",
            term="ahaṃkāra / adhyāsa",
            explanation=(
                f"A13: Y (the sākṣin) never perceives dualistically. The claim that "
                f"Y perceives {claimed_object!r} as an object is a violation — "
                f"the Subject is the witness in whom perception appears, not itself a "
                f"perceiving subject standing over against objects (W4: perceivers are "
                f"conditioned)."
            ),
            reframe=(
                "Model the observer-role as a conditioned jīva (Conditioned at Vyav), "
                "not as Y. The witness Y is that in which the jīva's perception appears."
            ),
        )
    return None


# --- A14: Collapsed knower-known-knowing in the Subject ------------------------

def check_a14_trinity_collapsed(subject: Obj, knower: bool, known: bool, knowing: bool) -> Violation | None:
    """A14 — Y is simultaneously Knower, Known, and Knowing (*tripuṭī* collapse).

    If ``subject`` is Y but any of the three roles is absent, A14 is violated.
    """
    if is_subject(subject) and not (knower and known and knowing):
        missing = [name for name, v in
                   [("Knower (jñātṛ)", knower), ("Known (jñeya)", known), ("Knowing (jñāna)", knowing)]
                   if not v]
        return Violation(
            axiom_id="A14",
            term="jñātṛ–jñeya–jñāna (tripuṭī)",
            explanation=(
                f"A14: in the Subject, Knower/Known/Knowing collapse into one. "
                f"Y is missing: {', '.join(missing)}. The Subject is not a partial "
                f"knower — the tripartite structure dissolves in Y (W7/W10)."
            ),
        )
    return None


# --- CH1–CH4: Change/permanence ------------------------------------------------

def check_ch1_absolute_unchanged(x: Obj, changes: bool) -> Violation | None:
    """CH1 — the Absolute does not change."""
    if is_absolute(x) and changes:
        return Violation(
            axiom_id="CH1",
            term="kūṭastha (immutable)",
            explanation=f"CH1: the Absolute does not change. {x!r} is the Absolute but is reported as changing.",
        )
    return None


def check_ch2_absolute_unborn(x: Obj, born: bool) -> Violation | None:
    """CH2 — the Absolute is not born."""
    if is_absolute(x) and born:
        return Violation(
            axiom_id="CH2",
            term="aja (unborn)",
            explanation=f"CH2: the Absolute is not born. {x!r} is the Absolute but is reported as born.",
        )
    return None


def check_ch3_absolute_undying(x: Obj, dies: bool) -> Violation | None:
    """CH3 — the Absolute does not die."""
    if is_absolute(x) and dies:
        return Violation(
            axiom_id="CH3",
            term="amṛta (deathless)",
            explanation=f"CH3: the Absolute does not die. {x!r} is the Absolute but is reported as dying.",
        )
    return None


def check_ch4_conditioned_mutable(x: Obj, is_vyav: bool, born_or_dies_or_changes: bool) -> Violation | None:
    """CH4 — a *vyāvahārika* Conditioned entity is subject to birth, death, or change."""
    if is_conditioned(x) and is_vyav and not born_or_dies_or_changes:
        return Violation(
            axiom_id="CH4",
            term="vikāra (modification)",
            explanation=(
                f"CH4: every Conditioned entity at the vyāvahārika level is born, "
                f"dies, or changes. {x!r} is Conditioned at Vyav but none of these "
                f"apply."
            ),
        )
    return None
