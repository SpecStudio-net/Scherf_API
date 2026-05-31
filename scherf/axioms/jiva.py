"""J-series and I-series axiom checks — jīva and Īśvara.

Source: ``JivaIsvara.lean`` (J1–J8, I1–I6, minus derived J3/J5/J9/J10/I3).

The jīva (individual subject) and Īśvara (cosmic/lord) are both Conditioned entities
at the *vyāvahārika* level. In witness-centered design, the jīva is the conventional
handle for "a person" in an interaction — not the user's ultimate identity (which is Y).
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned
from ..report import Violation
from ..sorts import Level, Obj


def check_j1_jiva_conditioned(jiva: Obj) -> Violation | None:
    """J1 — a jīva is Conditioned."""
    if not is_conditioned(jiva):
        return Violation(
            axiom_id="J1",
            term="jīva",
            explanation=f"J1: a jīva must be Conditioned. {jiva!r} is not Conditioned.",
        )
    return None


def check_j2_jiva_at_vyav(jiva: Obj, level: Level) -> Violation | None:
    """J2 — a jīva is at the *vyāvahārika* level."""
    if level is not Level.VYAV:
        return Violation(
            axiom_id="J2",
            term="jīva / vyāvahārika",
            explanation=(
                f"J2: a jīva exists at the vyāvahārika level. "
                f"{jiva!r} is assigned to {level.value}."
            ),
        )
    return None


def check_j6_jiva_has_ignorance(jiva: Obj, has_ignorance_of_absolute: bool) -> Violation | None:
    """J6 — a jīva has ignorance of the Absolute (avidyā)."""
    if not has_ignorance_of_absolute:
        return Violation(
            axiom_id="J6",
            term="avidyā",
            explanation=(
                f"J6: every jīva has ignorance of the Absolute "
                f"(∃a. A(a) ∧ IgnoranceOf(jīva, a)). {jiva!r} has none recorded."
            ),
        )
    return None


def check_j8_multiple_jivas(jiva_count: int) -> Violation | None:
    """J8 — at least two distinct jīvas exist."""
    if jiva_count < 2:
        return Violation(
            axiom_id="J8",
            term="jīva-bhedha",
            explanation=(
                f"J8: at least two distinct jīvas must exist "
                f"(∃j1 j2. Jiva(j1) ∧ Jiva(j2) ∧ j1 ≠ j2). Only {jiva_count} found."
            ),
        )
    return None


def check_i1_isvara_conditioned(isvara: Obj) -> Violation | None:
    """I1 — Īśvara is Conditioned."""
    if not is_conditioned(isvara):
        return Violation(
            axiom_id="I1",
            term="Īśvara",
            explanation=f"I1: Īśvara is Conditioned. {isvara!r} is not Conditioned.",
        )
    return None


def check_i2_isvara_at_vyav(isvara: Obj, level: Level) -> Violation | None:
    """I2 — Īśvara is at the *vyāvahārika* level."""
    if level is not Level.VYAV:
        return Violation(
            axiom_id="I2",
            term="Īśvara / vyāvahārika",
            explanation=(
                f"I2: Īśvara exists at the vyāvahārika level. "
                f"{isvara!r} is assigned to {level.value}."
            ),
        )
    return None


def check_i5_unique_isvara(isvara_count: int) -> Violation | None:
    """I5 — there is exactly one Īśvara."""
    if isvara_count != 1:
        return Violation(
            axiom_id="I5",
            term="Īśvara",
            explanation=(
                f"I5: Īśvara is unique (∀i1 i2. Isvara(i1) ∧ Isvara(i2) → i1 = i2). "
                f"{isvara_count} Īśvara entities found."
            ),
        )
    return None
