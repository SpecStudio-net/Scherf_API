"""Verification for engine.py + report.py.

Covers the application-facing API (Interaction / Claim / check / classify) and the
axiom routing (A13/M6/M7, EG1/EG2, AV18, AV22, A13/W4 stance check).

Run:  python3 tests/test_engine.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scherf.engine import Claim, Interaction, classify
from scherf.sorts import Level, State


def run() -> None:
    checks: list[str] = []

    def ok(msg: str) -> None:
        checks.append(msg)

    # 1. Clean interaction — no violations ----------------------------------------
    ix = Interaction()
    ix.assert_claim(
        Claim.about("alice").says("alice has a preference for plain language").at(Level.VYAV)
    )
    result = ix.check()
    assert result.ok, f"Expected ok, got: {result}"
    ok("Clean claim at VYAV produces no violations")

    # 2. adhyāsa — user IS their profile at Param (A13/M6/M7) ----------------------
    ix2 = Interaction()
    ix2.assert_claim(
        Claim.about("alice").says("user IS their preference profile").at(Level.PARAM)
    )
    result2 = ix2.check()
    assert not result2.ok, "Expected violation for Param identity claim"
    axiom_ids = [v.axiom_id for v in result2.violations]
    assert any("M6" in aid or "A13" in aid for aid in axiom_ids), f"Expected A13/M6/M7 violation, got: {axiom_ids}"
    ok("A13/M6/M7 — user-IS-profile at Param is flagged as adhyāsa")

    # 3. EG1/EG2 — profiling stance ------------------------------------------------
    ix3 = Interaction()
    ix3.assert_claim(Claim.system_stance("steer user toward predicted choice"))
    result3 = ix3.check()
    assert not result3.ok, "Expected violation for profiling/steering stance"
    ok("A13/W4 — 'steer/predict' stance flagged as objectifying the user")

    # 4. EG1/EG2 on identity claim -------------------------------------------------
    ix4 = Interaction()
    ix4.assert_claim(
        Claim.about("alice").says("build behavioral profile of user").at(Level.VYAV)
    )
    result4 = ix4.check()
    assert not result4.ok
    assert any("EG" in v.axiom_id for v in result4.violations), "Expected EG violation"
    ok("EG1/EG2 — 'behavioral profile' claim flagged as ahaṃkāra construction")

    # 5. AV18 — user in state at Param --------------------------------------------
    ix5 = Interaction()
    ix5.assert_claim(
        Claim.about("alice").says("user is waking, that is their ultimate nature").at(Level.PARAM)
    )
    result5 = ix5.check()
    assert not result5.ok
    assert any("AV18" in v.axiom_id for v in result5.violations)
    ok("AV18 — placing user 'in a state' at Param level is flagged (turīya)")

    # 6. AV22 on output level — transient output claimed as Param ------------------
    ix6 = Interaction()
    ix6.assert_claim(
        Claim.output("The optimal response for this user is X")
              .says("The optimal response for this user is X")
              .manifests_in(State.JAGRAT)
              .absent_from(State.SUSUPTI)
              .at(Level.PARAM)
    )
    result6 = ix6.check()
    assert not result6.ok
    assert any("AV22" in v.axiom_id for v in result6.violations)
    ok("AV22 — context-dependent output claimed at Param is flagged")

    # 7. classify() — no state info defaults to VYAV ------------------------------
    lvl = classify("The user asked about Python.")
    assert lvl is Level.VYAV
    ok("classify() — no transience info → VYAV (conventional)")

    # 8. classify() — transient content → PRAT ------------------------------------
    lvl2 = classify(
        "This appeared in waking only.",
        present_in={State.JAGRAT},
        absent_in={State.SUSUPTI},
    )
    assert lvl2 is Level.PRAT
    ok("classify() — transient content (state-dependent) → PRAT (apparent)")

    # 9. Report is human-legible (has axiom_id, term, explanation) -----------------
    ix7 = Interaction()
    ix7.assert_claim(Claim.about("u").says("user IS their profile").at(Level.PARAM))
    r = ix7.check()
    v = r.violations[0]
    assert v.axiom_id and v.term and v.explanation
    assert v.reframe  # a reframe should always be present for design-doc demo
    ok("Report structure — each Violation has axiom_id, term, explanation, reframe")

    print(f"Engine: {len(checks)} checks passed\n")
    for i, c in enumerate(checks, 1):
        print(f"  {i:>2}. {c}")


if __name__ == "__main__":
    run()
