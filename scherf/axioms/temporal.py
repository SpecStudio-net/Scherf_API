"""T-series axiom checks — temporal ordering.

Source: ``TemporalAxioms.lean`` (T1–T6). Time is a strict linear order in this
formalization. The Absolute has no events (E10) and hence no temporal properties
(A7a) — time is a Conditioned, vyāvahārika structure (ST2/ST4).
"""

from __future__ import annotations

from ..report import Violation


def check_t1_irreflexive(t: object, before_self: bool) -> Violation | None:
    """T1 — Before is irreflexive: ¬Before(t, t)."""
    if before_self:
        return Violation(
            axiom_id="T1",
            term="kāla (time ordering)",
            explanation=f"T1: Before is irreflexive — no time instant is before itself. {t!r} is before itself.",
        )
    return None


def check_t2_transitive(t1: object, t2: object, t3: object,
                         t1_before_t2: bool, t2_before_t3: bool,
                         t1_before_t3: bool) -> Violation | None:
    """T2 — Before is transitive: Before(t1,t2) ∧ Before(t2,t3) → Before(t1,t3)."""
    if t1_before_t2 and t2_before_t3 and not t1_before_t3:
        return Violation(
            axiom_id="T2",
            term="kāla (transitivity)",
            explanation=(
                f"T2: Before is transitive. {t1!r} < {t2!r} and {t2!r} < {t3!r} "
                f"but {t1!r} is not before {t3!r}."
            ),
        )
    return None


def check_t3_asymmetric(t1: object, t2: object,
                         t1_before_t2: bool, t2_before_t1: bool) -> Violation | None:
    """T3 — Before is asymmetric: Before(t1,t2) → ¬Before(t2,t1)."""
    if t1_before_t2 and t2_before_t1:
        return Violation(
            axiom_id="T3",
            term="kāla (asymmetry)",
            explanation=f"T3: Before is asymmetric. {t1!r} and {t2!r} are mutually before each other.",
        )
    return None


def check_t4_linear(t1: object, t2: object,
                     t1_before_t2: bool, t2_before_t1: bool) -> Violation | None:
    """T4 — Before is linear: distinct instants are ordered (Before(t1,t2) ∨ Before(t2,t1))."""
    if t1 is not t2 and not t1_before_t2 and not t2_before_t1:
        return Violation(
            axiom_id="T4",
            term="kāla (linearity)",
            explanation=(
                f"T4: distinct time instants must be ordered. {t1!r} and {t2!r} are "
                f"distinct but neither is before the other."
            ),
        )
    return None
