"""Smoke tests for the mechanical axiom modules (core, levels, maya, jiva, awareness,
additional, temporal, event). One test per series, exercising both the satisfied and
violated paths.

Run:  python3 tests/test_axioms.py
"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scherf import SELF, conventional, apparent, Level, State
from scherf.axioms import core, levels as lv, maya, jiva, awareness, additional, temporal, event


def run() -> None:
    checks: list[str] = []
    def ok(msg: str) -> None: checks.append(msg)

    person = conventional("alice")
    dream_obj = apparent("mirage")

    # --- core ------------------------------------------------------------------
    assert core.check_a1(SELF) is None
    assert core.check_a1(person) is None
    ok("A1 — partition holds for SELF and Conditioned")

    assert core.check_a4(SELF) is None
    ok("A4 — SELF passes Y↔A check")

    v = core.check_a13(SELF, person)
    assert v is not None and "A13" in v.axiom_id
    assert core.check_a13(person, SELF) is None
    ok("A13 — Y perceiving is a violation; jīva perceiving is not")

    assert core.check_ch1_absolute_unchanged(SELF, changes=False) is None
    v2 = core.check_ch1_absolute_unchanged(SELF, changes=True)
    assert v2 is not None and "CH1" in v2.axiom_id
    ok("CH1 — Absolute changing is a violation")

    assert core.check_ch4_conditioned_mutable(person, is_vyav=True, born_or_dies_or_changes=True) is None
    ok("CH4 — Conditioned at Vyav with change is fine")

    # --- levels ----------------------------------------------------------------
    assert lv.check_k2(SELF, Level.PARAM) is None
    v3 = lv.check_k2(SELF, Level.VYAV)
    assert v3 is not None and "K2" in v3.axiom_id
    ok("K2 — Absolute not at Param is a violation")

    v4 = lv.check_k3(person, Level.PARAM)
    assert v4 is not None and "K3" in v4.axiom_id
    assert lv.check_k3(person, Level.VYAV) is None
    ok("K3 — Conditioned at Param is a violation")

    assert lv.check_k5_sublation(Level.VYAV, Level.PRAT) is None
    v5 = lv.check_k5_sublation(Level.PRAT, Level.VYAV)
    assert v5 is not None and "K5" in v5.axiom_id
    ok("K5 — Prat sublating Vyav is a violation")

    # --- maya ------------------------------------------------------------------
    assert maya.check_m6_superimposed_is_conditioned(person) is None
    v6 = maya.check_m6_superimposed_is_conditioned(SELF)
    assert v6 is not None and "M6" in v6.axiom_id
    ok("M6 — SELF as superimposed is a violation")

    assert maya.check_m7_substrate_is_absolute(SELF) is None
    v7 = maya.check_m7_substrate_is_absolute(person)
    assert v7 is not None and "M7" in v7.axiom_id
    ok("M7 — Conditioned as substrate is a violation")

    assert maya.check_m8_substrate_unchanged(SELF, real_change_asserted=False) is None
    v8 = maya.check_m8_substrate_unchanged(SELF, real_change_asserted=True)
    assert v8 is not None and "M8" in v8.axiom_id
    ok("M8 — real change in SELF (asaṅga violation) is caught")

    assert maya.check_m12_ignorance_of_absolute(SELF) is None
    v9 = maya.check_m12_ignorance_of_absolute(person)
    assert v9 is not None and "M12" in v9.axiom_id
    ok("M12 — avidyā of a Conditioned entity is a violation")

    assert maya.check_m15_absolute_no_ignorance(person) is None
    v10 = maya.check_m15_absolute_no_ignorance(SELF)
    assert v10 is not None and "M15" in v10.axiom_id
    ok("M15 — ignorance attributed to the Absolute is a violation")

    # --- jiva ------------------------------------------------------------------
    assert jiva.check_j1_jiva_conditioned(person) is None
    v11 = jiva.check_j1_jiva_conditioned(SELF)
    assert v11 is not None and "J1" in v11.axiom_id
    ok("J1 — SELF as jīva is a violation")

    assert jiva.check_j2_jiva_at_vyav(person, Level.VYAV) is None
    v12 = jiva.check_j2_jiva_at_vyav(person, Level.PRAT)
    assert v12 is not None and "J2" in v12.axiom_id
    ok("J2 — jīva at Prat is a violation")

    assert jiva.check_i5_unique_isvara(1) is None
    v13 = jiva.check_i5_unique_isvara(2)
    assert v13 is not None and "I5" in v13.axiom_id
    ok("I5 — two Īśvaras is a violation")

    # --- awareness -------------------------------------------------------------
    assert awareness.check_w4_perceiver_conditioned(person) is None
    v14 = awareness.check_w4_perceiver_conditioned(SELF)
    assert v14 is not None and "W4" in v14.axiom_id
    ok("W4 — Absolute as perceiver is a violation")

    assert awareness.check_w6_perception_requires_distinctness(person, dream_obj) is None
    v15 = awareness.check_w6_perception_requires_distinctness(person, person)
    assert v15 is not None and "W6" in v15.axiom_id
    ok("W6 — self-perception is a violation")

    assert awareness.check_w11_witness_of_all_is_absolute(SELF, witnesses_all=True) is None
    v16 = awareness.check_w11_witness_of_all_is_absolute(person, witnesses_all=True)
    assert v16 is not None and "W11" in v16.axiom_id
    ok("W11 — non-Absolute witnessing all is a violation")

    # --- additional ------------------------------------------------------------
    assert additional.check_eg1_ego_conditioned(person) is None
    v17 = additional.check_eg1_ego_conditioned(SELF)
    assert v17 is not None and "EG1" in v17.axiom_id
    ok("EG1 — SELF as Ego is a violation")

    assert additional.check_eg2_ego_identifies_with_body(True, True, True) is None
    v18 = additional.check_eg2_ego_identifies_with_body(True, False, True)
    assert v18 is not None and "EG2" in v18.axiom_id
    ok("EG2 — Ego missing Body is a violation")

    assert additional.check_g2_absolute_transcends_guna(SELF, has_guna=False) is None
    v19 = additional.check_g2_absolute_transcends_guna(SELF, has_guna=True)
    assert v19 is not None and "G2" in v19.axiom_id
    ok("G2 — guṇa attributed to Absolute is a violation")

    assert additional.check_u2_absolute_no_upadhi(person) is None
    v20 = additional.check_u2_absolute_no_upadhi(SELF)
    assert v20 is not None and "U2" in v20.axiom_id
    ok("U2 — upādhi on Absolute is a violation")

    # --- temporal --------------------------------------------------------------
    assert temporal.check_t1_irreflexive("t1", before_self=False) is None
    v21 = temporal.check_t1_irreflexive("t1", before_self=True)
    assert v21 is not None and "T1" in v21.axiom_id
    ok("T1 — a time before itself is a violation")

    assert temporal.check_t3_asymmetric("t1", "t2", True, False) is None
    v22 = temporal.check_t3_asymmetric("t1", "t2", True, True)
    assert v22 is not None and "T3" in v22.axiom_id
    ok("T3 — mutual Before is a violation")

    # --- event -----------------------------------------------------------------
    assert event.check_e10_absolute_no_events(SELF, has_events=False) is None
    v23 = event.check_e10_absolute_no_events(SELF, has_events=True)
    assert v23 is not None and "E10" in v23.axiom_id
    ok("E10 — events on the Absolute is a violation")

    assert event.check_e9_causal_ordering("t1", "t2", cause_before_effect=True) is None
    v24 = event.check_e9_causal_ordering("t1", "t2", cause_before_effect=False)
    assert v24 is not None and "E9" in v24.axiom_id
    ok("E9 — effect before cause is a violation")

    print(f"Axiom modules: {len(checks)} checks passed\n")
    for i, c in enumerate(checks, 1):
        print(f"  {i:>2}. {c}")


if __name__ == "__main__":
    run()
