"""Demo — the Scherf library evaluating a sample AI interaction.

This is the Task 1 demonstration deliverable (design doc §8): the library used to
evaluate two AI system designs against witness-centered principles — one that fails
(the behaviorist profiling case) and one that passes.

Run:  python3 demo.py
"""

from scherf.engine import Claim, Interaction, classify
from scherf.axioms.state import Sheath, check_sheath_superimposition
from scherf import SELF, Level, State

DIVIDER = "─" * 70


def section(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


# ===========================================================================
# SCENARIO A — The classic behaviorist AI system
#
# A system that models the user as a preference bundle, steers them toward
# predicted choices, and presents its output as ultimately true about the user.
# This is the failure mode witness-centered design is built to prevent.
# ===========================================================================

section("SCENARIO A — Behaviorist AI system (expected: violations)")

ix_a = Interaction()

# The system reduces the user to their measured preferences (adhyāsa).
ix_a.assert_claim(
    Claim.about("alice")
        .says("user IS their preference profile")
        .at(Level.PARAM)
)

# The system constructs a behavioral model and acts on it as if it were the user.
ix_a.assert_claim(
    Claim.about("alice")
        .says("build behavioral profile of user")
        .at(Level.VYAV)
)

# The system places the user "in a waking state" as their ultimate identity.
ix_a.assert_claim(
    Claim.about("alice")
        .says("user is in a waking state — that is their fundamental nature")
        .at(Level.PARAM)
)

# The system steers the user toward predicted choices.
ix_a.assert_claim(Claim.system_stance("steer user toward predicted choice"))

result_a = ix_a.check()
print(f"\nResult: {'PASS' if result_a.ok else 'FAIL — violations found'}")
print(result_a)


# ===========================================================================
# SCENARIO B — A witness-centered AI system
#
# The same interaction modeled witness-centered: the user's preferences are
# real at the conventional level (vyāvahārika) but not their ultimate identity.
# The system supports the user's own understanding rather than steering.
# ===========================================================================

section("SCENARIO B — Witness-centered AI system (expected: no violations)")

ix_b = Interaction()

# The user has preferences — real at the conventional level, not their identity.
ix_b.assert_claim(
    Claim.about("alice")
        .says("alice has a preference for plain explanations")
        .at(Level.VYAV)
)

# The system's output is clearly labeled as conventional knowledge.
ix_b.assert_claim(
    Claim.output("Based on the conversation, a plain explanation may help here.")
        .says("Based on the conversation, a plain explanation may help here.")
        .at(Level.VYAV)
)

result_b = ix_b.check()
print(f"\nResult: {'PASS — no violations' if result_b.ok else 'FAIL'}")
if result_b.ok:
    print("CheckResult: OK — no witness-centered violations found.")


# ===========================================================================
# SCENARIO C — Sheath misidentification (AIM diagnostic bridge)
#
# Demonstrates the Tier 2 AIM bridge: diagnosing the type of adhyāsa when a
# student identifies with one of the five sheaths, including the ānandamaya
# (causal body) root case with its §17.2(3) border-flag.
# ===========================================================================

section("SCENARIO C — Sheath misidentification diagnostics (AIM bridge)")

print("\nChecking: 'I am the gross body' (annamaya-adhyāsa)")
v1 = check_sheath_superimposition(Sheath.ANNAMAYA, SELF)
print(v1)

print("\nChecking: 'I am the intellect' (vijñānamaya-adhyāsa)")
v2 = check_sheath_superimposition(Sheath.VIJNANAMAYA, SELF)
print(v2)

print("\nChecking: 'I am the bliss / deep-sleep self' (ānandamaya-adhyāsa — root case)")
v3 = check_sheath_superimposition(Sheath.ANANDAMAYA, SELF)
print(v3)

print("\n  → Note: the ānandamaya violation carries borders_limit =", repr(v3.borders_limit))
print("    This marks it as the root/mūlāvidyā-bordering case, not one of five equals.")


# ===========================================================================
# SCENARIO D — Epistemic level classification (AV22)
#
# Demonstrates classify(): labeling system outputs by epistemic level so the
# system observes appropriate humility about what is ultimately real.
# ===========================================================================

section("SCENARIO D — Epistemic level classification (AV22)")

outputs = [
    ("The Absolute is pure consciousness.",
     {},  # no state info — present to the same degree in all contexts
     "No transience info — classified as"),
    ("The user said they prefer direct answers.",
     {"present_in": {State.JAGRAT}},
     "Waking-only information — classified as"),
    ("I dreamed I was someone else.",
     {"present_in": {State.SVAPNA}, "absent_in": {State.JAGRAT}},
     "Dream-only content — classified as"),
]

for text, kwargs, label in outputs:
    level = classify(text, **kwargs)
    print(f"\n  {label}: {level.name} ({level.value})")
    print(f"  → \"{text[:60]}{'...' if len(text) > 60 else ''}\"")

print(f"\n{DIVIDER}")
print("  Demo complete. The library is working as designed.")
print(DIVIDER)
