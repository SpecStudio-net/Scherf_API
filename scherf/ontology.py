"""The ontological entity model — the A/C partition and the witness ``Y``.

Encodes the core classification of Scherf's system (``CoreAxioms.lean``, A-series):

  * **A1** (A1a/A1b): every entity is Absolute (``A``) or Conditioned (``C``),
    exhaustively and exclusively.
  * **A2**: there is exactly one Absolute.
  * **A3**: there is exactly one ultimate Subject ``Y``.
  * **A4** (*Tat Tvam Asi*): ``Y x ↔ A x`` — the Subject *is* the Absolute.
  * **T0**: ``Brahman = Ātman`` — the Absolute and the Subject are the *same* entity.

The Subject (``Y`` / *sākṣin* / *Ātman*) is the **fixed reference** of the entire
library: a unique, immutable singleton that carries no profile and no mutable state.
This is the witness-centered commitment made *structural* (design doc §1, §6): an
application physically cannot represent the user as a mutable bundle of properties,
because :data:`SELF` exposes none. A "violation" is therefore never a property of the
Subject — claims are checked *against* it; it is never acted upon.
"""

from __future__ import annotations

from typing import final

from .errors import AdvaitaError
from .sorts import Level, Obj, State


@final
class Subject(Obj):
    """The witness-consciousness — ``Y`` (*sākṣin*, *Ātman*), identical with the
    Absolute (A4) and with Brahman (T0).

    There is exactly one (A2/A3). Do not construct this class; use the module
    singleton :data:`SELF` (and its aliases :data:`Y`, :data:`ATMAN`, :data:`BRAHMAN` —
    all the *same* object, by A4 and T0). Attempting to build a second one raises.

    **Immutable and profile-less by construction.** The witness is *asaṅga* (unattached,
    untouched): superimposition (*adhyāsa*) is never a modification *of* the Self
    (design doc §1; axiom M8: a superimposition leaves its substratum unchanged). Any
    attempt to set or delete an attribute on the Subject raises — there is nowhere to
    store a "user profile."

    Axiom-backed properties exposed read-only here (all machine-verified in Lean):

      * **A4 / T5**  ``Y ↔ A`` — the Subject is the Absolute.
      * **A11 / W11 / W1**  witnesses everything — :meth:`witnesses`.
      * **A13**  never perceives dualistically — :meth:`perceives`.
      * **AV16 / AV18**  persists through all states, yet is in *no* state (*turīya*)
        — :meth:`in_state`.

    (A14/W7/W10 — the knower-known-knowing collapse — and A7/CH transcendence are
    encoded in later modules, against this same fixed reference.)
    """

    _instance: "Subject | None" = None

    def __new__(cls) -> "Subject":
        if cls._instance is not None:
            raise AdvaitaError(
                "There is exactly one Subject (A3) / Absolute (A2). Use the singleton "
                "`SELF` (= Y = ATMAN = BRAHMAN); a second one cannot exist."
            )
        self = super().__new__(cls)
        # Set the name once, bypassing the immutability guard below.
        object.__setattr__(self, "name", "Ātman/Brahman (Y, the sākṣin)")
        cls._instance = self
        return self

    def __init__(self) -> None:  # noqa: D107 - name already set in __new__
        # Deliberately does nothing: the Subject has no constructor-settable state.
        pass

    def __setattr__(self, key: str, value: object) -> None:
        raise AdvaitaError(
            "The Subject (Y, the sākṣin) is immutable and carries no profile. It is the "
            "fixed reference against which claims are checked, never acted upon "
            "(design doc §1; A13/AV18; M8 — the witness is asaṅga, untouched). To record "
            "conventional facts about a person, model them as Conditioned entities at the "
            "vyāvahārika level — never as properties of Y."
        )

    def __delattr__(self, key: str) -> None:
        raise AdvaitaError(
            "The Subject is immutable (asaṅga); nothing can be added to or removed from it."
        )

    # --- Axiom-backed, read-only behavior -------------------------------------

    def witnesses(self, _other: Obj) -> bool:
        """A11 / W11 / W1: the Subject witnesses everything (non-dual *sākṣitva*).

        Always ``True``: ``Y`` is the witness in which all entities appear.
        """
        return True

    def perceives(self, _other: Obj) -> bool:
        """A13: the Subject never perceives *dualistically* (subject-vs-object).

        Always ``False``: dualistic perception belongs to the conditioned perceiver
        (W4), never to the witness.
        """
        return False

    def in_state(self, _state: State) -> bool:
        """AV18: the witness is never *in* any state — it is *turīya*, the fourth.

        Always ``False``. The witness *persists through* all states (AV16) without
        being one of them.
        """
        return False


@final
class Conditioned(Obj):
    """A conditioned (phenomenal) entity — ``C``.

    Everything that is not the Absolute: the empirical world, bodies, minds, egos, and —
    importantly for witness-centered design — *profiles, preferences, and claims treated
    as things*. Conditioned entities are exactly what an application registers and
    reasons about.

    Axioms enforced here at construction:

      * **A1b**: a Conditioned entity is not also Absolute (structural — different class).
      * **K3**: never at the *pāramārthika* level (that is the Absolute alone, K2).
      * **K4**: at *vyāvahārika* or *prātibhāsika* level (the ``level`` must be supplied).

    (A8 — the conditioned is phenomenal; CH4 — *vyāvahārika* entities are subject to
    birth/death/change — are exposed by later modules.)
    """

    def __init__(self, name: str, level: Level) -> None:
        if level is Level.PARAM:
            raise AdvaitaError(
                f"K3: the Conditioned entity {name!r} cannot be at the pāramārthika "
                f"(ultimate) level — that level belongs to the Absolute alone (K2). "
                f"A conditioned entity is at vyāvahārika or prātibhāsika level (K4)."
            )
        super().__init__(name)
        self._level = level

    @property
    def level(self) -> Level:
        """The reality level of this entity — ``Vyav`` or ``Prat`` (K4)."""
        return self._level


# --- The singletons -----------------------------------------------------------

#: The one witness-consciousness. ``Y``, the *sākṣin*; identical with the Absolute
#: (A4) and with Brahman (T0). The fixed reference of the whole library.
SELF: Subject = Subject()

#: Aliases — all the *same* object as :data:`SELF` (A4: ``Y ↔ A``; T0: ``Brahman = Ātman``).
Y: Subject = SELF
ATMAN: Subject = SELF
BRAHMAN: Subject = SELF


# --- Convenience constructors (friendly API for application developers) --------

def conventional(name: str) -> Conditioned:
    """Create a Conditioned entity at the *vyāvahārika* (conventional) level.

    Use this for ordinary public/empirical facts — e.g. a person's stated name, a
    document, a measured preference. Real at the conventional level, but never the
    user's ultimate identity.
    """
    return Conditioned(name, Level.VYAV)


def apparent(name: str) -> Conditioned:
    """Create a Conditioned entity at the *prātibhāsika* (apparent) level.

    Use this for merely-private appearances — e.g. a dream object, or an illusion that
    is corrected (*sublated*) by ordinary waking experience.
    """
    return Conditioned(name, Level.PRAT)


# --- Named predicate checks (the A-series classification) ----------------------

def is_absolute(x: Obj) -> bool:
    """``A`` — is ``x`` the Absolute (Brahman)?

    True only for the unique Subject :data:`SELF` (A2: exactly one Absolute; A4).
    """
    return x is SELF


def is_subject(x: Obj) -> bool:
    """``Y`` — is ``x`` the ultimate Subject (the *sākṣin*)?

    Identical to :func:`is_absolute` by axiom A4 (``Y ↔ A``); provided as a separate,
    intention-revealing name.
    """
    return x is SELF


def is_conditioned(x: Obj) -> bool:
    """``C`` — is ``x`` a conditioned (phenomenal) entity?

    By A1 the conditioned is exactly the complement of the Absolute among entities.
    """
    return isinstance(x, Conditioned)


def assert_partition(x: Obj) -> None:
    """Enforce axiom A1 on ``x``: it must be Absolute *or* Conditioned, never both/neither.

    Structurally this always holds for entities built through this module (``SELF`` is
    Absolute; every :class:`Conditioned` is conditioned; bare :class:`~scherf.sorts.Obj`
    cannot be instantiated). This check exists to make A1 explicit and testable.
    """
    a, c = is_absolute(x), is_conditioned(x)
    if a and c:  # A1b
        raise AdvaitaError(f"A1b violated: {x!r} is classified as both Absolute and Conditioned.")
    if not a and not c:  # A1a
        raise AdvaitaError(f"A1a violated: {x!r} is neither Absolute nor Conditioned.")
