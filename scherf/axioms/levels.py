"""K-series axiom checks — the three levels of reality.

Source: ``LevelAxioms.lean`` (K1–K6). These are largely enforced structurally by
:mod:`scherf.levels`; named here for explicit coverage.
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned
from ..report import Violation
from ..sorts import Level, Obj


def check_k1(x: Obj, assigned_level: Level | None) -> Violation | None:
    """K1 — every entity is at exactly one of Param / Vyav / Prat."""
    if assigned_level is None:
        return Violation(
            axiom_id="K1",
            term="pāramārthika / vyāvahārika / prātibhāsika",
            explanation=f"K1: {x!r} has no level assigned; every entity must be at one of the three levels.",
        )
    return None


def check_k2(x: Obj, assigned_level: Level) -> Violation | None:
    """K2/K2a/K2b — the Absolute is at Param only (never Vyav or Prat)."""
    if is_absolute(x) and assigned_level is not Level.PARAM:
        return Violation(
            axiom_id="K2",
            term="pāramārthika",
            explanation=(
                f"K2: the Absolute is at the pāramārthika level only. "
                f"{x!r} is the Absolute but assigned to {assigned_level.value}."
            ),
        )
    return None


def check_k3(x: Obj, assigned_level: Level) -> Violation | None:
    """K3 — the Conditioned is never at Param."""
    if is_conditioned(x) and assigned_level is Level.PARAM:
        return Violation(
            axiom_id="K3",
            term="pāramārthika",
            explanation=(
                f"K3: the Conditioned is never at the pāramārthika (ultimate) level — "
                f"that belongs to the Absolute alone. {x!r} is Conditioned but placed at Param."
            ),
            reframe="Assign to vyāvahārika (Level.VYAV) or prātibhāsika (Level.PRAT).",
        )
    return None


def check_k4(x: Obj, assigned_level: Level) -> Violation | None:
    """K4 — the Conditioned is at Vyav or Prat."""
    if is_conditioned(x) and assigned_level is Level.PARAM:
        return check_k3(x, assigned_level)  # same condition, delegate
    return None


def check_k5_sublation(higher_level: Level, lower_level: Level) -> Violation | None:
    """K5 — hierarchical sublation: Vyav sublates Prat, not the reverse."""
    if higher_level is Level.PRAT and lower_level is Level.VYAV:
        return Violation(
            axiom_id="K5",
            term="bādha (sublation)",
            explanation=(
                "K5: sublation is hierarchical — vyāvahārika sublates prātibhāsika, "
                "not the reverse. A prātibhāsika entity cannot sublate a vyāvahārika one."
            ),
        )
    return None
