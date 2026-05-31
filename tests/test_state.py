"""Verification for axioms/state.py — the AV-series and the sheath superimposition,
with focused checks on the ānandamaya (causal-body) border-flag (ruling (b)).

Run:  python3 tests/test_state.py
"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scherf import SELF, conventional, State
from scherf.axioms import state as st
from scherf.axioms.state import Sheath, ANANDAMAYA_LIMIT


def run() -> None:
    checks: list[str] = []
    def ok(msg: str) -> None: checks.append(msg)

    person = conventional("alice")

    # --- Sheath superimposition: the four ordinary sheaths ----------------------
    for sheath in [Sheath.ANNAMAYA, Sheath.PRANAMAYA, Sheath.MANOMAYA, Sheath.VIJNANAMAYA]:
        v = st.check_sheath_superimposition(sheath, SELF)
        assert v is not None, f"{sheath} on SELF should be diagnosed"
        assert v.axiom_id == "M6/M7", f"{sheath} should be plain M6/M7"
        assert not v.borders_limit, f"{sheath} should NOT border a limit"
    ok("M6/M7 — the four ordinary sheath superimpositions are diagnosed, no border-flag")

    # --- Sheath superimposition: ānandamaya is flagged as the root case ---------
    va = st.check_sheath_superimposition(Sheath.ANANDAMAYA, SELF)
    assert va is not None, "ānandamaya on SELF should be diagnosed"
    assert "AV15" in va.axiom_id, "ānandamaya should cite AV15 (causal body / seed of ignorance)"
    assert va.borders_limit == ANANDAMAYA_LIMIT, "ānandamaya MUST border the §17.2(3) mūlāvidyā limit"
    assert "mūlāvidyā" in va.term or "ānandamaya" in va.term
    assert "root" in va.explanation.lower(), "ānandamaya explanation must mark it as the root case"
    ok("M6/M7 + AV15 — ānandamaya superimposition flagged as bordering §17.2(3) mūlāvidyā (ruling b)")

    # --- The border-flag is visible in the rendered report ----------------------
    rendered = str(va)
    assert "⚠" in rendered and "root case" in rendered, "border-flag must surface in str(Violation)"
    ok("Render — the ānandamaya border-flag surfaces in the human-readable report")

    # --- M7 guard: a non-Absolute substrate is not a sheath-on-Self error -------
    assert st.check_sheath_superimposition(Sheath.ANANDAMAYA, person) is None
    ok("M7 — sheath superimposed on a Conditioned substrate is not a Self-misidentification")

    # --- Sheath body associations ----------------------------------------------
    assert "causal body" in Sheath.ANANDAMAYA.body
    assert Sheath.ANANDAMAYA.is_root and not Sheath.MANOMAYA.is_root
    ok("Sheath — ānandamaya maps to the causal body and is the root sheath")

    # --- AV1: unique state ------------------------------------------------------
    assert st.check_av1_unique_state(person, 1) is None
    assert st.check_av1_unique_state(person, 2) is not None
    ok("AV1 — a jīva must be in exactly one state")

    # --- AV11: deep sleep — nothing manifests -----------------------------------
    assert st.check_av11_deep_sleep_no_manifestation(State.SUSUPTI, manifests_something=False) is None
    v11 = st.check_av11_deep_sleep_no_manifestation(State.SUSUPTI, manifests_something=True)
    assert v11 is not None and "AV11" in v11.axiom_id
    assert st.check_av11_deep_sleep_no_manifestation(State.JAGRAT, manifests_something=True) is None
    ok("AV11 — manifestation in deep sleep is a violation; in waking it is fine")

    # --- AV15: causal body persists in suṣupti ----------------------------------
    assert st.check_av15_causal_body_persists(State.SUSUPTI, causal_body_persists=True) is None
    v15 = st.check_av15_causal_body_persists(State.SUSUPTI, causal_body_persists=False)
    assert v15 is not None and "AV15" in v15.axiom_id
    ok("AV15 — the causal body (seed of ignorance) must persist in deep sleep")

    # --- AV18: witness never in a state -----------------------------------------
    assert st.check_av18_witness_no_state(SELF, in_some_state=False) is None
    v18 = st.check_av18_witness_no_state(SELF, in_some_state=True)
    assert v18 is not None and "AV18" in v18.axiom_id
    assert st.check_av18_witness_no_state(person, in_some_state=True) is None
    ok("AV18 — claiming Y is in a state is a violation; the jīva in a state is fine")

    # --- AV22 / AV23: criterion of reality --------------------------------------
    v22 = st.check_av22_criterion(SELF, manifests_in_one_state=True, absent_in_another_state=True)
    assert v22 is not None and "AV22" in v22.axiom_id
    assert st.check_av23_absolute_no_manifestation(SELF, manifests=True) is not None
    ok("AV22/AV23 — the Absolute is never transient and never empirically manifests")

    # --- AV24/25: bodies and world are Conditioned ------------------------------
    assert st.check_av24_av25_conditioned(person, "gross body") is None
    v24 = st.check_av24_av25_conditioned(SELF, "gross body")
    assert v24 is not None and "AV24" in v24.axiom_id
    ok("AV24/AV25 — bodies/world must be Conditioned; SELF as a body is a violation")

    print(f"State module: {len(checks)} checks passed\n")
    for i, c in enumerate(checks, 1):
        print(f"  {i:>2}. {c}")


if __name__ == "__main__":
    run()
