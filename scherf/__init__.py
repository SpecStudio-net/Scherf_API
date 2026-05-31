"""scherf — a domain-agnostic, witness-centered model of the sentient user.

A transparent software encoding of Matthew Scherf's machine-verified Lean 4
formalization of Advaita Vedānta (README v5.0.0; 129 axioms across ten modules). The
library models the user as the *sākṣin* — the witnessing subject ``Y`` — rather than as
a behavioral profile, and lets an AI application check whether its claims and responses
are consistent with witness-centered principles.

See ``docs/task1-design.md`` for the design, and ``docs/axiom-catalogue.md`` for the
authoritative axiom reference.

**Module 1 (this checkpoint)** provides the ontological substrate:

  * :mod:`scherf.sorts`     — the five sorts and the Level/State constants.
  * :mod:`scherf.ontology`  — the A/C partition and the immutable witness ``SELF`` (``Y``).
  * :mod:`scherf.levels`    — ``Level_of``, sublation (K5), and the AV22 reality criterion.

The application-facing claim/check API (``Interaction``, ``Claim``, ``check``,
``classify`` — design doc §7) is added in the engine checkpoint, on top of this model.
"""

from __future__ import annotations

from .errors import AdvaitaError
from .levels import (
    appears_transient_so_not_absolute,
    is_at,
    level_of,
    sublates,
    transient,
)
from .ontology import (
    ATMAN,
    BRAHMAN,
    SELF,
    Y,
    Conditioned,
    Subject,
    apparent,
    assert_partition,
    conventional,
    is_absolute,
    is_conditioned,
    is_subject,
)
from .sorts import Event, Level, Obj, State, Time

__all__ = [
    # errors
    "AdvaitaError",
    # sorts
    "Obj",
    "Level",
    "State",
    "Time",
    "Event",
    # ontology — entities
    "Subject",
    "Conditioned",
    "SELF",
    "Y",
    "ATMAN",
    "BRAHMAN",
    "conventional",
    "apparent",
    # ontology — predicates
    "is_absolute",
    "is_subject",
    "is_conditioned",
    "assert_partition",
    # levels
    "level_of",
    "is_at",
    "sublates",
    "transient",
    "appears_transient_so_not_absolute",
]
