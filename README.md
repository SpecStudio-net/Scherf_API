# Scherf_API — Witness-Centered AI Foundation Library

A Python library that gives AI applications a formal model of what a human being is,
grounded in Matthew Scherf's machine-verified Lean 4 formalization of Advaita Vedānta.

Most AI interaction systems are built on an implicit behaviorist premise: the user is
a bundle of preferences and behaviors to be modeled and optimized. This produces
documented failure modes — cognitive dependency, learning atrophy, and the erosion of
independent judgment.

**Witness-centered design** is an architectural alternative. Its central principle:
the user is the *sākṣin* — the witnessing subject in whom the interaction appears —
not reducible to any behavioral profile. A system designed to serve this knowing
subject looks and behaves differently from one designed to optimize for outcomes.

This library encodes that alternative as software, derived from a formal axiom system
that has been machine-verified in Lean 4.

---

## Formal foundation

[Matthew Scherf's formalization](https://github.com/matthew-scherf/Advaita) of
Advaita Vedānta in Lean 4 — the first machine-verified formalization of a non-Western
philosophical system — comprises **129 primitive axioms** across ten modules:

- Core metaphysics (A-series): identity of Ātman and Brahman; the exhaustive
  partition into Absolute and Conditioned
- Level axioms (K-series): three ontological levels — *pāramārthika*, *vyāvahārika*,
  *prātibhāsika* — with hierarchical sublation
- Māyā axioms (M-series): superimposition (*adhyāsa*), appearance (*vivarta*),
  ignorance (*avidyā*)
- Awareness axioms (W-series): witnessing vs. dualistic perception; the
  knower-known-knowing collapse in the Subject
- Ego axioms (EG-series): the formal model of misidentification — an ego is a
  conditioned *apparent subject* that identifies with a body
- State axioms (AV-series): the three-state analysis (*avasthā-traya*) and the
  witness-consciousness (*sākṣin*) that persists through all three
- Plus J/I, U/G, S, T, E, CH, ST, CA series

All proofs are machine-verified. The library encodes these axioms as named, readable
Python checks — it does not re-prove consistency, which Lean has already established.

---

## What the library does

**It checks claims.** Before your system acts on an assertion about the user — *the
user IS their preference profile*, *steer the user toward this predicted choice* — you
can ask whether that claim is consistent with witness-centered principles. If it is
not, the library names the violated axiom, explains the issue in plain language, and
suggests a reframe.

**It classifies outputs.** Using the three-level framework (AV22: what appears in one
context and not another cannot be ultimately real), the library labels system outputs
by epistemic level — distinguishing conventional knowledge from ultimately real claims.

**It models the user as the witness.** `SELF` (also `Y`, `ATMAN`, `BRAHMAN`) is a
singleton constant representing the user. It is immutable — you cannot add a profile
to it, and the type system enforces this. Conventional facts about a person are
modeled as separate conditioned entities at the *vyāvahārika* level.

---

## Quick example

```python
from scherf.engine import Claim, Interaction, classify
from scherf import Level

# A claim your system is about to act on:
ix = Interaction()
ix.assert_claim(
    Claim.about("alice")
        .says("user IS their preference profile")
        .at(Level.PARAM)
)
result = ix.check()

# Result is a report, not an exception:
for v in result.violations:
    print(v.axiom_id, "—", v.term)
    print(v.explanation)
    print("Reframe:", v.reframe)
```

Output:
```
A13/M6/M7 — adhyāsa
The claim identifies the user (→ Y, the sākṣin) with a conditioned property
at the ultimate (pāramārthika) level. This is adhyāsa — superimposition of
the conditioned upon the Absolute witness ...
Reframe: Model 'alice' as a Conditioned entity at vyāvahārika level ...
```

Run `python3 demo.py` for a full four-scenario demonstration.

---

## Project structure

```
scherf/           The library
  sorts.py        Five sorts (Obj, Level, State, Time, Event) and constants
  ontology.py     The A/C partition; SELF (Y/Ātman/Brahman) as immutable singleton
  levels.py       Level_of, sublation (K5), the AV22 reality criterion
  engine.py       Interaction / Claim / check() / classify() — the application API
  report.py       Violation and CheckResult
  errors.py       AdvaitaError (ontology-integrity errors only)
  axioms/         One module per axiom series (core, levels, maya, jiva, awareness,
                  additional, temporal, event, state)
  README.md       Developer reference (no Advaita background required)

demo.py           Four-scenario demonstration
tests/            56 axiom-cited checks across four test files

docs/
  task1-design.md       Full design document with rationale for every decision
  axiom-catalogue.md    All 129 axioms reconciled from the Lean source
  limits.md             What the formalism cannot capture and how the library marks it
  opus-briefing-package.md  Project briefing (Tasks 1–3)
```

---

## Requirements

Python 3.11+. No external dependencies for the core library.

---

## Relationship to AIM

The [Advaita Inquiry Matrix](https://github.com/SpecStudio-net/Advaita-Inquiry-Matrix)
(AIM) is a structured AI-assisted pedagogy engine for Advaita Vedānta teaching. This
library is being built as its formal foundation — the General Theory against which
AIM's diagnostic logic, state machine, and *prakriyā* selection will be audited and
validated (Tasks 2 and 3 of the project).

---

## Licence

Apache 2.0 — see [LICENSE](LICENSE).

## Author

Dev Bhagavān / [SpecStudio](https://specstudio.net) — hello@specstudio.net
