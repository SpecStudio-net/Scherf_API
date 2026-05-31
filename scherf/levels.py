"""The three-level reality system — ``Level_of``, sublation, and the reality criterion.

Encodes the K-series (``LevelAxioms.lean``) together with the AV22 criterion of reality:

  * **K1**: every entity is at one of ``Param`` / ``Vyav`` / ``Prat``.
  * **K2** (K2a/K2b): the Absolute is at ``Param`` only (never ``Vyav`` / ``Prat``).
  * **K3**: the Conditioned is never at ``Param``.
  * **K4**: the Conditioned is at ``Vyav`` or ``Prat``.
  * **K5**: hierarchical sublation — a ``Vyav`` entity *sublates* (*bādha*) a ``Prat``
    entity. (Asymmetry of sublation overall is axiom M18, in the *māyā* module.)
  * **K6**: the ``Vyav`` level is non-empty.
  * **AV22** (criterion of reality): whatever appears in one state but not another
    cannot be the Absolute — *transience ⇒ non-Absolute*.

This is the framework an application uses for the *epistemic classification* of its
outputs (design doc §7.3): labeling a claim ``Param`` / ``Vyav`` / ``Prat`` so the
system can observe appropriate epistemic humility.
"""

from __future__ import annotations

from .errors import AdvaitaError
from .ontology import Conditioned, is_absolute, is_conditioned
from .sorts import Level, Obj, State


def level_of(x: Obj) -> Level:
    """``Level_of`` — the reality level of entity ``x``.

    Realizes K1/K2/K3/K4 directly:

      * the Absolute (``SELF``) is at ``Param`` (K2), and only there (K2a/K2b);
      * a :class:`~scherf.ontology.Conditioned` entity reports its own ``Vyav`` /
        ``Prat`` level (K3 forbids ``Param``; K4 guarantees one of the lower two).
    """
    if is_absolute(x):
        return Level.PARAM
    if isinstance(x, Conditioned):
        return x.level
    # By A1 every entity is Absolute or Conditioned; nothing else should reach here.
    raise AdvaitaError(
        f"K1/A1: cannot assign a level to {x!r} — it is neither the Absolute nor a "
        f"Conditioned entity."
    )


def is_at(x: Obj, level: Level) -> bool:
    """Is ``x`` at the given reality ``level``? (``Level_of(x, level)``.)"""
    return level_of(x) is level


def sublates(higher: Obj, lower: Obj) -> bool:
    """``Sublates`` (*bādha*) at the level hierarchy — axiom K5.

    True iff ``higher`` is a Conditioned ``Vyav`` entity and ``lower`` is a ``Prat``
    entity: the conventional cancels/corrects the merely-apparent (as waking experience
    sublates a dream). Returns ``False`` otherwise; in particular sublation is
    asymmetric — ``Prat`` never sublates ``Vyav`` (cf. M18).

    Note: this is *level-based* sublation (K5). The general sublation relation over
    *knowledges* (M16–M18, including liberating knowledge) is in the *māyā* module.
    """
    return (
        is_conditioned(higher)
        and level_of(higher) is Level.VYAV
        and level_of(lower) is Level.PRAT
    )


def transient(present_in: set[State], absent_in: set[State]) -> bool:
    """Is something *transient* — manifest in some state(s) and absent in others?

    A helper for the AV22 criterion below. Empty inputs mean "no information," which is
    not transience.
    """
    return bool(present_in) and bool(absent_in)


def appears_transient_so_not_absolute(
    x: Obj,
    *,
    present_in: set[State],
    absent_in: set[State],
) -> bool:
    """``AV22`` — the criterion of reality.

    If ``x`` manifests in one state but not another (it is *transient*), then it
    cannot be the Absolute: *what comes and goes is not ultimately real*. Returns
    ``True`` when AV22 forces the conclusion "``x`` is not Absolute" (i.e. ``x`` is at
    most a conditioned appearance).

    This is the formal basis for classifying system outputs by epistemic level: a claim
    that holds only in some contexts and not others is at best ``Vyav`` / ``Prat``,
    never ``Param``.

    Guard: by AV23 the Absolute never manifests empirically, so the genuine Subject is
    never "present in" a state to begin with. If it is reported as transient, that is a
    contradiction in the inputs, and we say so rather than silently mis-classify.
    """
    is_transient = transient(present_in, absent_in)
    if is_transient and is_absolute(x):
        raise AdvaitaError(
            "AV22/AV23 contradiction: the Absolute (Y) never manifests in a state "
            "(AV23), so it cannot be reported as appearing in one state and not "
            "another. Re-examine the inputs — `x` cannot be both the Absolute and "
            "transient."
        )
    return is_transient
