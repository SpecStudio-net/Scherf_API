"""Verification for Module 1 — sorts, ontology (A/C partition + witness), levels.

Plain-assert checks, standard library only. Run directly:

    python3 tests/test_module1.py

Each check states the axiom it verifies. The point of Module 1 is that the
witness-centered commitments are *structural* — the type system refuses to build an
ontology that contradicts the axioms — so several checks assert that an illegal
construction raises.
"""

from __future__ import annotations

import os
import sys

# Make the project root importable when run as a plain script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scherf as s  # noqa: E402
from scherf import AdvaitaError, Level, State  # noqa: E402


def expect_error(fn, label: str) -> None:
    try:
        fn()
    except AdvaitaError:
        return
    raise AssertionError(f"expected AdvaitaError but none raised: {label}")


def run() -> None:
    checks: list[str] = []

    def ok(msg: str) -> None:
        checks.append(msg)

    # --- A2/A3: exactly one Subject/Absolute; it is the singleton ---------------
    assert s.SELF is s.Y is s.ATMAN is s.BRAHMAN, "A4/T0: Y = A = Ātman = Brahman, one object"
    ok("A4/T0  — SELF, Y, ATMAN, BRAHMAN are the one same entity")
    expect_error(s.Subject, "A2/A3: constructing a second Subject")
    ok("A2/A3  — a second Subject/Absolute cannot be constructed")

    # --- A1: Obj is abstract; every entity is Absolute XOR Conditioned ----------
    expect_error(lambda: s.Obj("rogue"), "A1a: bare Obj is abstract")
    ok("A1a    — a bare Obj (neither A nor C) cannot exist")

    person = s.conventional("alice")  # a jīva-level handle, NOT the user's true Self
    assert s.is_conditioned(person) and not s.is_absolute(person)
    assert s.is_absolute(s.SELF) and s.is_subject(s.SELF) and not s.is_conditioned(s.SELF)
    s.assert_partition(s.SELF)
    s.assert_partition(person)
    ok("A1/A4  — SELF is Absolute=Subject; a conventional handle is Conditioned")

    # --- Witness is immutable and profile-less (the core invariant) -------------
    expect_error(lambda: setattr(s.SELF, "preferences", {"x": 1}), "no profile on Y")
    expect_error(lambda: setattr(s.SELF, "name", "renamed"), "Y immutable")
    expect_error(lambda: delattr(s.SELF, "name"), "Y nothing removable")
    ok("A13/AV18/M8 — the witness Y is immutable and carries no profile (asaṅga)")

    # --- A11/A13/AV18: read-only witness behavior -------------------------------
    assert s.SELF.witnesses(person) is True, "A11/W11: witnesses everything"
    assert s.SELF.perceives(person) is False, "A13: never perceives dualistically"
    assert all(s.SELF.in_state(st) is False for st in State), "AV18: in no state (turīya)"
    ok("A11/A13/AV18 — Y witnesses all, perceives nothing dualistically, is in no state")

    # --- K2/K3/K4: levels --------------------------------------------------------
    assert s.level_of(s.SELF) is Level.PARAM, "K2: Absolute at pāramārthika"
    assert s.level_of(person) is Level.VYAV, "K4: conventional handle at vyāvahārika"
    assert s.level_of(s.apparent("mirage")) is Level.PRAT, "K4: apparent at prātibhāsika"
    expect_error(lambda: s.Conditioned("bad", Level.PARAM), "K3: conditioned cannot be Param")
    ok("K2/K3/K4 — Absolute at Param only; Conditioned at Vyav/Prat, never Param")

    # --- K5 / M18-direction: sublation is asymmetric ----------------------------
    waking = s.conventional("waking-cup")     # Vyav
    dream = s.apparent("dream-cup")            # Prat
    assert s.sublates(waking, dream) is True, "K5: Vyav sublates Prat"
    assert s.sublates(dream, waking) is False, "asymmetry: Prat does not sublate Vyav"
    ok("K5     — vyāvahārika sublates prātibhāsika, and not vice versa")

    # --- AV22: criterion of reality ---------------------------------------------
    assert s.appears_transient_so_not_absolute(
        dream, present_in={State.SVAPNA}, absent_in={State.JAGRAT}
    ) is True, "AV22: appears in dream, gone in waking ⇒ not Absolute"
    assert s.appears_transient_so_not_absolute(
        dream, present_in=set(), absent_in=set()
    ) is False, "AV22: no transience information ⇒ no conclusion"
    expect_error(
        lambda: s.appears_transient_so_not_absolute(
            s.SELF, present_in={State.JAGRAT}, absent_in={State.SUSUPTI}
        ),
        "AV22/AV23: the Absolute never manifests in a state",
    )
    ok("AV22/AV23 — transience ⇒ non-Absolute; the Absolute is never reported transient")

    print(f"Module 1: {len(checks)} checks passed\n")
    for i, c in enumerate(checks, 1):
        print(f"  {i:>2}. {c}")


if __name__ == "__main__":
    run()
