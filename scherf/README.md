# scherf — Witness-Centered AI Foundation Library

A Python library that gives AI applications a formal model of what a human being is,
grounded in Matthew Scherf's machine-verified Lean 4 formalization of Advaita Vedānta
(129 axioms, fully proven). It replaces the implicit behaviorist premise of most AI
systems — *the user is a bundle of preferences to be optimized* — with an explicit,
examined alternative: *the user is the witnessing subject in whom the interaction
appears*.

You do not need to know Advaita Vedānta to use this library. You need to understand
two ideas:

**1. The user is the witness, not the profile.**
The library models the user as `SELF` — a constant that cannot be profiled, modified,
or put into a state. Conventional facts about a person (their preferences, history,
current task) are real and useful, but they are modeled as *conditioned* entities that
appear to the witness, never as the witness itself.

**2. Claims can be checked.**
Before your system acts on a claim about the user — *the user IS their behavioral
profile*, *steer the user toward this choice* — you can ask the library whether that
claim is consistent with witness-centered principles. If it is not, the library tells
you which axiom it violates and how to reframe it.

---

## Installation

No external dependencies. Python 3.11+ required.

```bash
git clone <repo>
cd scherf
```

All imports are from the `scherf` package:

```python
import scherf
from scherf.engine import Claim, Interaction, classify
```

---

## Quick start

### Checking a claim

```python
from scherf.engine import Claim, Interaction
from scherf import Level

ix = Interaction()

# Register a claim your system is about to act on.
ix.assert_claim(
    Claim.about("alice")
        .says("user IS their preference profile")
        .at(Level.PARAM)   # claiming this is ultimately true of the user
)

result = ix.check()

if not result.ok:
    for v in result.violations:
        print(v.axiom_id, v.term)
        print(v.explanation)
        print("Reframe:", v.reframe)
```

Output:
```
A13/M6/M7  adhyāsa
The claim 'user IS their preference profile' identifies the user (→ Y, the
sākṣin) with a conditioned property at the ultimate (pāramārthika) level ...
Reframe: Model 'alice' as a Conditioned entity at vyāvahārika level ...
```

A **violation is never raised as an exception** — it is a structured report with a
human-readable explanation. Your system can log it, surface it to a reviewer, or
route it to a different response path.

### Checking a system stance

```python
ix.assert_claim(Claim.system_stance("steer user toward predicted choice"))
```

This flags the `A13/W4` (*ahaṃkāra*) violation: treating the user as an object to be
steered rather than a subject to be served.

### Classifying an output's epistemic level

```python
from scherf.engine import classify
from scherf import State, Level

# Without state information: defaults to vyāvahārika (conventional knowledge).
level = classify("The user asked about Python.")
# → Level.VYAV

# With state information: applies the transience criterion (AV22).
level = classify(
    "I dreamed I was someone else.",
    present_in={State.SVAPNA},
    absent_in={State.JAGRAT},
)
# → Level.PRAT  (merely apparent — present in dream, absent in waking)
```

The three levels:
- `Level.PARAM` — ultimate reality. Never returned for a system output; reserved for
  the Absolute alone. If your system labels something `Param`, it will be flagged.
- `Level.VYAV` — conventional reality. The right label for most empirical knowledge,
  preferences, and situational facts.
- `Level.PRAT` — apparent reality. Context-dependent appearances: valid in one
  situation, absent in another.

---

## Core concepts

### `SELF` — the witness (Y, Ātman, Brahman)

The user is `SELF`. It is a singleton constant — there can only be one — and it is
immutable: you cannot add properties to it, and trying to do so raises immediately.

```python
from scherf import SELF, Y, ATMAN, BRAHMAN
# All four names refer to the same object.

SELF.witnesses(anything)   # always True  (A11)
SELF.perceives(anything)   # always False (A13)
SELF.in_state(any_state)   # always False (AV18 — turīya)
```

This is not a convention. The type system enforces it: `SELF` has nowhere to store a
profile because none of the attributes exist.

### `Conditioned` entities — conventional facts about a person

Ordinary facts about a person are `Conditioned` entities at the conventional level.
They are real and useful; they just are not the user's ultimate identity.

```python
from scherf import conventional, apparent

person_handle = conventional("alice")    # vyāvahārika — shared empirical fact
dream_object  = apparent("mirage")       # prātibhāsika — merely apparent
```

### Sheath misidentification (for AIM / pedagogy applications)

```python
from scherf.axioms.state import Sheath, check_sheath_superimposition
from scherf import SELF

v = check_sheath_superimposition(Sheath.ANANDAMAYA, SELF)
# Returns a Violation identifying this as the root (mūlāvidyā-bordering) case.
print(v.borders_limit)
# → '§17.2(3) — anādi-avidyā (mūlāvidyā: the beginninglessness of ignorance)'
```

The five sheaths in diagnostic order (subtlest last):
| Sheath | IAST | Body | `Sheath` constant |
|--------|------|------|-------------------|
| Food / physical | annamaya-kośa | Gross body | `Sheath.ANNAMAYA` |
| Vital | prāṇamaya-kośa | Subtle body | `Sheath.PRANAMAYA` |
| Mental | manomaya-kośa | Subtle body | `Sheath.MANOMAYA` |
| Intellectual | vijñānamaya-kośa | Subtle body | `Sheath.VIJNANAMAYA` |
| Bliss (root) | ānandamaya-kośa | Causal body | `Sheath.ANANDAMAYA` |

The *ānandamaya* case is flagged as the root — it borders the formalization limit on
the beginninglessness of *avidyā*. See `docs/limits.md` for the full account.

---

## The three-part API

| Call | What it does | Key axioms |
|------|-------------|-----------|
| `Interaction.assert_claim(Claim...)` | Register a claim | — |
| `Interaction.check()` | Evaluate against axioms; returns `CheckResult` | A13, M6/M7, EG1/EG2, AV18, AV22 |
| `classify(text, ...)` | Classify output by epistemic level | AV22, K2/K3 |

`CheckResult` has:
- `.ok` — `True` if no violations
- `.violations` — list of `Violation` objects (each with `.axiom_id`, `.term`,
  `.explanation`, `.reframe`, `.borders_limit`)

---

## Running the demo

```bash
python3 demo.py
```

Shows four scenarios: a failing behaviorist system, a passing witness-centered system,
the five sheath diagnostics (with the *ānandamaya* root-case flag), and epistemic
level classification.

## Running the tests

```bash
python3 tests/test_module1.py   # ontology / levels
python3 tests/test_engine.py    # claim checking / classify
python3 tests/test_axioms.py    # all axiom series
python3 tests/test_state.py     # AV-series + sheath superimposition
```

---

## Formal basis

The library encodes all 129 primitive axioms of Scherf's formalization across ten
series (A, K, M, J/I, W, U/G/EG/ST/CH, S, T, E, AV). Full catalogue:
`docs/axiom-catalogue.md`. Design rationale: `docs/task1-design.md`.

The axiom system is machine-verified in Lean 4.12.0. The library does not re-prove
that consistency — Lean already has. It checks whether specific claims and interaction
states are consistent with the axioms, and reports the results in plain language.
