"""Sorts and constants — the type system of Scherf's signature.

Mirrors ``AdvaitaVedanta/Signature.lean`` (README v5.0.0 §1). Scherf's system has five
primitive *sorts*: ``Obj`` (entities), ``Level`` (reality levels), ``State`` (states
of consciousness), ``Time``, and ``Event``. This module provides the type system for
all five; the concrete entity model (the Absolute/Subject and Conditioned entities)
lives in :mod:`scherf.ontology`, and the three-level reality machinery in
:mod:`scherf.levels`.

A note on the fourth, *turīya*: it is **not** a member of :class:`State`. The witness's
transcendence of the three states (waking/dream/deep-sleep) is modeled as a property of
the Subject ``Y`` (axiom AV18: the witness is never *in* any state), not as a state
value. See :mod:`scherf.ontology`.
"""

from __future__ import annotations

from enum import Enum
from typing import final

from .errors import AdvaitaError


@final
class Level(Enum):
    """The ``Level`` sort — the three ontological levels of reality (K-series).

    Lean: ``axiom Level : Type`` with constants ``Param``, ``Vyav``, ``Prat``.

    These are the levels at which something can be *real*. They are ranked: a higher
    level *sublates* (``bādha``, cancels/corrects) a lower one — see
    :func:`scherf.levels.sublates`.
    """

    PARAM = "pāramārthika"  # ultimate reality — the Absolute alone (K2)
    VYAV = "vyāvahārika"    # conventional reality — the shared empirical world
    PRAT = "prātibhāsika"   # apparent reality — private/illusory appearance (e.g. a dream object)

    @property
    def gloss(self) -> str:
        """A one-line plain-language gloss, for human-readable reports."""
        return {
            Level.PARAM: "ultimate (pāramārthika) — true of the Absolute alone",
            Level.VYAV: "conventional (vyāvahārika) — the shared, public empirical world",
            Level.PRAT: "apparent (prātibhāsika) — merely-private appearance, e.g. a dream object",
        }[self]


@final
class State(Enum):
    """The ``State`` sort — the three states of consciousness (*avasthā-traya*, AV-series).

    Lean: ``axiom State : Type`` with constants ``Jagrat``, ``Svapna``, ``Susupti`` and
    pairwise-distinctness axioms (``State_distinct_*``). Distinctness is automatic here:
    distinct enum members are unequal.

    *turīya* (the fourth) is intentionally absent — see the module docstring.
    """

    JAGRAT = "jāgrat"    # waking
    SVAPNA = "svapna"    # dream
    SUSUPTI = "suṣupti"  # deep sleep

    @property
    def gloss(self) -> str:
        return {
            State.JAGRAT: "waking (jāgrat) — gross body and shared world manifest",
            State.SVAPNA: "dream (svapna) — only mind-projected objects manifest",
            State.SUSUPTI: "deep sleep (suṣupti) — nothing manifests; only the causal body persists",
        }[self]


class Obj:
    """The ``Obj`` sort — the domain of entities (objects, subjects, states of affairs).

    Lean: ``axiom Obj : Type``.

    ``Obj`` is **abstract**: it is never instantiated directly. Axiom A1 (A1a/A1b) says
    every entity is either Absolute *or* Conditioned, exhaustively and exclusively, so
    every concrete entity must be a :class:`scherf.ontology.Subject` (the unique
    Absolute) or a :class:`scherf.ontology.Conditioned`. Trying to build a bare ``Obj``
    raises — the partition is enforced by the type system, not merely documented.
    """

    name: str

    def __new__(cls, *args: object, **kwargs: object) -> "Obj":
        if cls is Obj:
            raise AdvaitaError(
                "Obj is abstract (axiom A1): every entity is either the Absolute "
                "(the unique Subject, `SELF`) or a Conditioned entity. Construct a "
                "Conditioned entity, or use the SELF singleton — never a bare Obj."
            )
        return super().__new__(cls)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


@final
class Time:
    """The ``Time`` sort — temporal instants (``axiom Time : Type``).

    A placeholder marker at this stage. The temporal ordering relation ``Before`` and
    the T-series axioms (strict linear order) are implemented in the temporal module.
    """


@final
class Event:
    """The ``Event`` sort — occurrences (``axiom Event : Type``).

    A placeholder marker at this stage. Event existence/occurrence (``EE``, ``OccursAt``)
    and the E-series axioms are implemented in the event module.
    """
