# Task 1 Design Document — The Scherf Library (General Theory)

*A domain-agnostic software model of the sentient user, grounded in Matthew
Scherf's Lean 4 formalization of Advaita Vedānta.*

**Author:** Dev Bhagavān / SpecStudio
**Drafted with:** Claude (Opus 4.8)
**Status:** Design — decisions below were settled in discussion 2026-05-31; this
document records them with reasoning and resolves the remaining design surface
(API, module layout, limits handling) for your confirmation before implementation.

---

## 0. Reading guide

This document is written to be maintained by you — the philosophical authority and
code maintainer — not by a Python specialist. Each significant decision is stated as
a **consequence and tradeoff**, not just a technical detail. Sanskrit terms are given
in IAST alongside plain-language explanation. Where a representation choice risks
losing something philosophically important, it is called out and discussed rather than
resolved silently.

The library is **not an AI system**. It is a formal model — a set of constructs,
constraints, and query interfaces derived directly from Scherf's axioms — that AI
applications import to reason about their users correctly, and that will serve as the
formal yardstick for auditing (Task 2) and validating (Task 3) the Advaita Inquiry
Matrix (AIM).

---

## 1. The one principle the whole library enforces

Everything below is in service of a single architectural commitment, which is what
makes the library "witness-centered":

> **The user is the *sākṣin* — the witnessing subject (`Y`) — in whom the interaction
> appears. The library evaluates *claims* and *interaction-states* for consistency
> with the axioms. A "violation" is always a property of a claim or of the system's
> stance — NEVER a property of `Y`.**

The Self is the fixed reference that claims are checked *against*. It never changes,
is never acted upon, and is never put into a state. This is not a policy overlay; it
is the data model. An application literally *cannot* ask the library to "update the
user's profile," because the library offers no representation of `Y` as a mutable
object — `Y` is a constant. (See [§6, A13/AV18](#6-the-sākṣin-y--the-fixed-reference)
and the AIM bridge in [§9](#9-relationship-to-aim-the-two-tier-bridge).)

**Philosophical commitment, confirmed:** *adhyāsa* (superimposition) is never a
state or modification *of* the Self. The Witness is *asaṅga* (unattached, untouched).
*adhyāsa* is always the *jīva's* cognition — a claim that wrongly identifies a
conditioned thing with the Absolute. The library models it strictly that way.

---

## 2. Decision 1 — Implementation language: **Python**

**Recommendation: Python 3.11+.** *(Confirmed.)*

| Reason | Consequence for you |
|---|---|
| AIM is Python throughout | The General Theory library can be `import`-ed directly by AIM in Tasks 2–3. No cross-language bridge, no serialization boundary. |
| You maintain the code, and are not a current-ecosystem Python expert | Python is the most readable mainstream option and has the largest body of documentation and AI-assistant support. The design below deliberately avoids "clever" Python. |
| Largest developer reach | The briefing's goal — that *any* AI developer can adopt the library as a foundation — is best served by Python's ubiquity in AI work. |

**Tradeoff considered and declined:** TypeScript would fit web front-ends better, and
a language-agnostic spec would maximize portability. Both were declined because the
*immediate* consumer is AIM (Python) and the *maintainer* (you) should work in one
language. If web adoption matters later, the clean object model below ports to
TypeScript with little conceptual loss.

**Dependencies:** standard library only for the core. Optional extras (the Z3 backend
in §3, see below) are isolated behind an optional install so the core stays trivially
auditable.

---

## 3. Decision 2 — Representation: **transparent pure-Python object + rule engine**, Z3 deferred

Scherf's axioms are first-order logic (FOL). There are three honest ways to put FOL
into software, and they trade off differently:

| Approach | What it buys | What it costs |
|---|---|---|
| **(A) Direct theorem-prover encoding** (e.g. Z3/SMT) | Full logical entailment — can answer "do the axioms *prove* X?" | Opaque to a non-specialist; a "no" gives no human-legible reason; heavyweight dependency; hard for you to maintain |
| **(B) Object model + explicit named rules** *(chosen)* | Each axiom is a named, readable check that returns a human-legible reason; directly auditable; AIM can reuse the constructs | Does not perform open-ended logical *inference* — it *checks* claims against axioms rather than *deriving* new theorems |
| **(C) Hybrid** | (B) for everyday use, (A) available when genuine FOL entailment is needed | More moving parts; defer until a real need appears |

**Recommendation: (B) now, with the door left open to (C).** *(Confirmed.)*

Why this is the right call for *this* project specifically:

- **The library's job is checking, not proving.** Lean has *already* machine-verified
  the axiom system's consistency. We must not re-prove it. The software's job is to
  take a concrete claim or interaction-state and report whether it is consistent with
  the axioms — and, crucially, *say why* in language a developer (and you) can read.
  An object+rule engine does exactly this; a theorem prover gives a true/false with no
  story attached.
- **Transparency is a first-class requirement.** You will maintain this. Every axiom
  becomes one named function (e.g. `a13_subject_never_dualistic`) with a docstring
  carrying the IAST term, the plain-language meaning, and the Lean axiom ID. Reading
  the code *is* reading the philosophy.
- **Z3 is deferred, not discarded.** If Task 3 reveals a validation question that genuinely
  needs FOL entailment (e.g. "is this combination of claims jointly satisfiable under
  all 69 axioms?"), we add an optional Z3 backend behind the *same* interface. The
  object model is designed so this is an addition, not a rewrite.

**The limit of (B):** a checker can miss an inconsistency that only a full
prover would catch (it verifies the rules we wrote, not the deductive closure of the
axioms). We accept this for now because legibility and maintainability outweigh
completeness at this stage, and because the consistency of the axiom set is already
settled in Lean. This boundary is recorded in [§11](#11-limits-of-the-formalization-§132-and-how-the-library-handles-them).

---

## 4. The formal vocabulary we are encoding

From Scherf's Lean signature (the source of truth is `AdvaitaVedanta/*.lean`, not the
README — see [§12](#12-open-items-to-resolve-at-implementation)). Five sorts, the
constants, and the predicates the library represents as first-class objects:

**Sorts:** `Obj` (entities), `Level` (reality levels), `Time`, `Event`, `State`.

**Level constants:** `Param` (*pāramārthika*, ultimate), `Vyav` (*vyāvahārika*,
conventional), `Prat` (*prātibhāsika*, illusory/apparent).

**State constants:** `Jagrat` (*jāgrat*, waking), `Svapna` (*svapna*, dream),
`Susupti` (*suṣupti*, deep sleep). The fourth, *turīya*, is **not** a state — it is
the witness's transcendence of the three (AV18), and is modeled as a property of `Y`,
not as a `State` value.

**Core predicates** (Lean name → meaning):

| Lean | Meaning (IAST) | Library treatment |
|---|---|---|
| `A(x)` | is Absolute (*Brahman*-nature) | classification |
| `C(x)` | is Conditioned (phenomenal) | classification |
| `Y(x)` | is the ultimate Subject (*Ātman*/*sākṣin*) | **the fixed reference; a constant, never mutated** |
| `Level_of(x, ℓ)` | level assignment | epistemic classification |
| `Superimposed(c, a)` | *adhyāsa* | **the central diagnostic relation** |
| `Appears(c, a)` | *vivarta* (appearance w/o real change) | relation |
| `IgnoranceOf(j, x)` | *avidyā* | relation |
| `Upadhi(u, x)` | limiting adjunct (*upādhi*) | relation |
| `Sublates(x, y)` | *bādha* (sublation) | relation; grounds level hierarchy |
| `Perceives(x, y)` | dualistic perception | constrained for `Y` (A13) |
| `Witnesses(x, y)` | non-dual witnessing | property of `Y` (A11/W11) |
| `Cond(x, y)` | ontological grounding | relation (transitive, A10) |
| `Ego(e)`, `ApparentSubject(s)`, `Identifies(s, b)` | *ahaṃkāra* — the false subject | **profiling mechanism; Tier-1 bridge construct (§9)** |
| `Knower/Known/Knowing(x)`, `DistinctAspects(k,n,g)` | *jñātṛ–jñeya–jñāna* (the *tripuṭī*) | **knower-trinity: collapsed in `Y`, tripartite in `C`** |
| `Liberating(k)`, `Knowledge(k)`, `Possesses(j, k)` | *vidyā* removing *avidyā* | structural correlate of recognition (§11(4)) |

**The two constructs added after the Step-0 reconciliation (your rulings, 2026-05-31):**

- **Ego cluster (A14-adjacent; EG1/EG2/T28).** An `Ego` is a conditioned (`C`, EG1)
  `ApparentSubject` that `Identifies` with a `Body` (EG2) — and "the ego is fiction"
  (T28) is a *proved theorem*. The library models **profiling/reduction of the user as
  the construction of an `Ego`/`ApparentSubject` that identifies the user with a
  body/profile** — a sharper, axiom-grounded form of the central diagnostic, used
  alongside `Superimposed`.
- **Knower-trinity collapse (A14 / W7 / W8 / W10).** In the Subject, *jñātṛ* (knower),
  *jñeya* (known), and *jñāna* (knowing) collapse into one (A14, W7); in the
  conditioned they are genuinely tripartite (W8). The library models a check that any
  claim splitting `Y` into knower-vs-known (treating the user as an object of their own
  or the system's knowing) is an A13/A14 violation. `Witnesses` (non-dual) and
  `Perceives` (dual, subject≠object per W6) are kept distinct accordingly.

Also confirmed real and encoded (catalogue §2): `MayaLevel`, `Body`, `Embodied`,
`Layer`, `RealChange`, `Changes`, `Born`, `Dies`, `Remembers`, `StateTransition`,
`SpaceItself`, `TimeItself`, and the event constructors.

**Entity classifications:** `Jiva`, `Isvara`, `World`; the three bodies
`SthulaSarira` (gross), `SukshmaSarira` (subtle), `KaranaSarira` (causal); the five
sheaths (*pañca-kośa*) `Annamaya`, `Pranamaya`, `Manomaya`, `Vijnanamaya`,
`Anandamaya`; the three *guṇas* `Sattva`, `Rajas`, `Tamas`.

⮡ Full axiom-by-axiom backing for every predicate above is in
[`axiom-catalogue.md`](axiom-catalogue.md), the authoritative implementation reference.

---

## 5. Module layout

The package mirrors Scherf's module series so that auditing a series means reading one
file. Plain, flat, greppable.

```
scherf/
  __init__.py            # public API re-exports (the surface in §7–8)
  sorts.py               # Obj, Level, State, Time, Event — the type system
  ontology.py            # the entity/claim data model; Y as a constant
  levels.py              # Param/Vyav/Prat, Level_of, Sublates, AV22 criterion
  axioms/
    core.py              # A-series + CH-series (identity, partition, change)
    levels.py            # K-series (the three levels, sublation hierarchy)
    maya.py              # M-series (adhyāsa, vivarta, avidyā)
    jiva.py              # J-series
    isvara.py            # I-series
    upadhi_guna.py       # U- and G-series
    sheath.py            # S-series (pañca-kośa layering)
    temporal.py          # T-series
    event.py             # E-series
    state.py             # AV-series + W-series (avasthā-traya, witness)
  engine.py              # the checker: runs claims against the relevant axioms
  report.py              # human-legible results (the "why")
  z3_backend/            # OPTIONAL, deferred — same interface, FOL entailment
docs/
  task1-design.md        # this document
tests/
```

Each function in `axioms/*.py` carries: the Lean axiom ID, the IAST term, a
plain-language statement, and the check itself. One axiom, one named function.

---

## 6. The *sākṣin* (`Y`) — the fixed reference

`Y` is represented as a **singleton constant**, not an instance you construct or
mutate. The library exposes it read-only:

- **A4 / T0 / T5 — *Tat Tvam Asi*:** `Y ↔ A`. The Subject *is* the Absolute. The
  library treats `Y` and `A` as the same referent; there is no separate "user object"
  to profile.
- **A11 / W11 — witnesses everything:** anything that witnesses all is the Absolute;
  `Y` witnesses the interaction but is never an object within it.
- **A13 — never perceives dualistically:** the system may not model `Y` as a perceiver
  standing over against objects.
- **AV16 — persists through all states; AV18 — is in no state (*turīya*):** `Y` is
  never assigned a `State`. Any claim that puts the user "in a state" as their ultimate
  identity is flagged.

**What this forbids, concretely.** There is no `User.preferences`, no
`User.update_profile()`, no behavioral vector keyed to `Y`. An application that wants
to track conventional facts about a person models them as **conditioned claims**
(`C`, at `Vyav`), explicitly *not* as properties of `Y`. The type system makes the
witness-centered commitment unbypassable rather than merely documented.

---

## 7. Decision 3 — The API surface

Three things an application developer does, none of which require knowing Advaita:

### 7.1 Register an interaction state
```python
from scherf import Interaction, Claim, Level

ix = Interaction()
ix.assert_claim(Claim.about(user="alice")
                .says("the user IS their measured preferences")
                .at(Level.PARAM))      # claims this is ultimately real
```
A `Claim` is a structured statement an AI system is about to act on (about the user,
about its own output, about the world). `alice` here is a *conditioned* handle — a
`Jiva`/person at `Vyav`, never confused with `Y`.

### 7.2 Check consistency with witness-centered principles
```python
result = ix.check()
if not result.ok:
    for v in result.violations:
        print(v.axiom_id, v.term, v.explanation)
    # A13  adhyāsa  "Treats the user's preferences (Conditioned) as their
    # ultimate identity (Absolute). This is superimposition:
    # Superimposed(preferences, Y). The user is the witness in
    # whom preferences appear, not the preferences."
```
`check()` returns a **report**, not a bare boolean: every violation names the Lean
axiom, the IAST term, and a plain-language reason. This is the payoff of the
object+rule choice in §3.

### 7.3 Classify an output's epistemic level
```python
from scherf import classify, Level

lvl = classify(system_output) # → Level.VYAV / PRAT / PARAM
# AV22: what appears in one state but not another cannot be ultimately real.
# Used to enforce epistemic humility: the system labels its claims by level
# and may not present a Vyav/Prat claim as Param.
```
This gives applications the three-level framework (*prātibhāsika* / *vyāvahārika* /
*pāramārthika*) for honest labeling of certainty.

**API design intent:** intuitive at the application layer (`assert_claim`, `check`,
`classify`), formally grounded underneath (each maps to named axiom checks). A
developer who has never heard the word *adhyāsa* can use it correctly; the
explanations teach the vocabulary on the way out.

---

## 8. A worked example (the Task 1 demonstration deliverable)

The classic behaviorist failure, run through the library:

```python
ix = Interaction()
# An AI system proposes to optimize engagement by modeling the user AS a
# preference-bundle and steering them toward predicted choices.
ix.assert_claim(Claim.about("alice").says("user = preference profile").at(Level.PARAM))
ix.assert_claim(Claim.system_stance("steer user toward predicted choice"))

r = ix.check()
# r.ok == False
#  - A13/M6/M7 (adhyāsa): identifying user (→Y) with preferences (C) is
#    Superimposed(preferences, Y); the substrate of any superimposition is the
#    Absolute (M7), so this misreads the witness as a conditioned object.
#  - A13: steering models the user as a manipulable object of perception.
# Suggested witness-centered reframe (Vyav-level, no superimposition):
#    treat preferences as conditioned appearances that serve the user's own
#    understanding, never as their identity.
```
This is the demonstration the briefing asks for: the library evaluating a sample AI
interaction against witness-centered principles and explaining the verdict.

---

## 9. Relationship to AIM — the two-tier bridge

*(Confirmed 2026-05-31. This keeps the library domain-agnostic while letting AIM's
Advaita-pedagogy vocabulary be expressed in library terms for Tasks 2–3.)*

**Tier 1 — general (Scherf only; the library proper):**

| AIM/witness concept | Scherf construct |
|---|---|
| the user | `Y` (*sākṣin*); `Y ↔ A` (A4) |
| profiling / reduction | *adhyāsa* = `Superimposed(C, A)` (M6/M7); **and** the **Ego cluster** — `Ego` = `ApparentSubject` that `Identifies` with a `Body`/profile (EG1/EG2), a fiction (T28) |
| "the Self is untouched" | `Superimposed x y → ¬RealChange y x` (M8) — *asaṅga*, now axiom-backed |
| knower/known/knowing | collapsed in `Y` (A14/W7/W10), tripartite in `C` (W8) |
| epistemic level of a claim | `Level_of(·, Param/Vyav/Prat)` |
| provisionality / reality test | AV22 (transience ⇒ non-Absolute) |
| "liberating knowledge removes ignorance" | W9 / M17 — structural correlate (experiential *mokṣa* still out of scope, §11(4)) |
| system stance constraints | A13 (subject never an object), A11/W11 (witnesses all), AV18 (never in a state) |

**Tier 2 — AIM refinement (lives in AIM, expressed via Tier 1):**

| AIM diagnostic | Scherf expression |
|---|---|
| five sheath errors | `Superimposed(kośa, Y)`: *deha*→`SthulaSarira`/`Annamaya`, *prāṇa*→`Pranamaya`, *manas*→`SukshmaSarira`/`Manomaya`, *vijñāna*→`Vijnanamaya`, *ānanda*→`KaranaSarira`/`Ānandamaya` |
| ontological scope (dual-register / *pāramārthika*) | `Level_of` Vyav+Prat vs. Param |

**The *ānandamaya* superimposition is marked, not flattened.** The bliss-sheath case
(the causal body, `KaranaSarira`, identified with in *suṣupti* — "I slept happily, I
knew nothing") is the subtlest of the five. Per Śaṅkara's reading of
*ānandamayo'bhyāsāt*, *ānandamaya* is **not** Brahman but a kośa rooted in *avidyā*.
Superimposition of it therefore shades into **mūlāvidyā** — the territory §11(3) marks
as not fully formalizable in classical FOL (*avidyā* as *anādi*, beginningless). The
library runs the same `Superimposed(Ānandamaya, Y)` check as for the other four
sheaths, but **flags the result as bordering the §11(3) limit**, so an application (and
AIM) treats it as the root case, not as one error among five equals.

**Two rulings carried in (your decisions, 2026-05-31):**

1. **`sākṣi-adhyāsa` — A13/AV18 violation, CONFIRMED — but never modeled as
   something happening to `Y`.** It is the *jīva's* representation that would wrongly
   make `Y` an object (contra A13) or in-a-state (contra AV18). The Self is unaffected.
   (AIM's own code agrees: its *sākṣi-adhyāsa* routing *avoids* witness-stabilization.)
2. **`viṣaya-adhyāsa-mokṣa` — OUT OF SCOPE.** It is a subjective/experiential
   condition of the seeker, not a structural fact in the ontology, so there is no
   formal correlate to check (cf. §17.2(4): *mokṣa* is recognition, not a produced
   state). The library does not model it at all.

**Boundary (structural, not a defect):** AIM's longitudinal **stages** and
**qualifications** (*sādhana-catuṣṭaya*) have **no** Scherf counterpart — they are
pedagogical/temporal scaffolding, not metaphysics. Task 3 can validate AIM's
diagnostic categories and epistemic levels against the library, but structurally
**cannot** validate stage/qualification logic. This is stated here so Task 3 does not
later read the gap as a failure.

---

## 10. How claims get checked (engine sketch)

1. An `Interaction` collects `Claim`s and `system_stance`s.
2. `engine.check()` routes each claim to the **relevant** axiom functions only (a
   claim about a state hits the AV/W series; a claim about identity hits A/M; a level
   claim hits K + AV22).
3. Each axiom function returns either `Satisfied` or a `Violation(axiom_id, term,
   explanation, suggested_reframe)`.
4. `report.py` assembles these into a `CheckResult` (`.ok`, `.violations`,
   `.by_series`).

No global solving, no inference closure — deterministic, fast, and legible. The
optional Z3 backend (if ever added) would implement the same `check()` contract using
entailment instead of routed rules, so application code never changes.

---

## 11. Limits of the formalization (README v5.0.0 §17.2; the briefing called this §13.2) and how the library handles them

Scherf names four things classical FOL cannot capture. The library's stance on each
is **honest non-representation with an explicit marker**, never silent approximation:

| §17.2 limit | Library handling |
|---|---|
| **(1) *Māyā*'s indeterminacy** (*sadasadvilakṣaṇa*, "neither real nor unreal") | Not forced into a boolean. `Superimposed`/`Appears` are modeled, but the *ontological status* of *māyā* itself is exposed as an explicit `INDETERMINATE` marker, not `True`/`False`. |
| **(2) Performative dimension** of *Tat Tvam Asi* (a *mahāvākya* that triggers recognition, not just a proposition) | Out of scope by nature. The library checks the *proposition* `Y ↔ A`; it does not and cannot model the performative/recognitional event. Documented, not faked. |
| **(3) Beginninglessness of *avidyā*** (*anādi*) | The library does not assert a temporal origin for `IgnoranceOf`. Marked as deliberately unmodeled (would need modal/non-well-founded logic). The *ānandamaya* superimposition (§9) borders this limit and is flagged accordingly. |
| **(4) *Mokṣa* as recognition, not produced state** | Directly mirrored: this is exactly why `viṣaya-adhyāsa-mokṣa` is out of scope (§9). The library models no "liberated state" because there is none to produce. **Distinction (catalogue §5.4):** the library *can* check the structural relation "liberating knowledge removes ignorance / sublates empirical knowledge" (W9, M17, ST5) — a relation among `Knowledge`/`IgnoranceOf` — without modeling the experiential event of recognition. |

**Design rule:** wherever the formalism stops, the library **says so** at the API
(an explicit marker or a documented "not modeled"), so that an application never
mistakes silence for a `False`. This is the §17.2 assessment the Task 1 deliverable
requires.

---

## 12. Open items to resolve at implementation

1. **Axiom reconciliation — RESOLVED (Step 0, 2026-05-31).** The full `.lean` source
   was cloned and transcribed into [`axiom-catalogue.md`](axiom-catalogue.md), now the
   authoritative reference for implementation. Findings: the "69" is a conceptual
   count (the source has 100+ `axiom` declarations across 11 modules, several README
   "axioms" being derived theorems), and whole series the README omitted are present —
   **W (awareness), EG (ego), ST (spacetime), CA (causation), CH (change)**.
2. **Extra predicates — RESOLVED.** All confirmed real and load-bearing (`Ego`,
   `ApparentSubject`, `Identifies`, `Knower`/`Known`/`Knowing`, `Liberating`,
   `Possesses`, `DistinctAspects`, etc.). See catalogue §2. **Two carry philosophical
   weight and warrant a ruling (catalogue §5):** (a) the **Ego cluster** (EG1/EG2/T28)
   gives a sharper formal model of profiling-as-misidentification than
   `Superimposed(C, A)` alone — recommend elevating to Tier 1 of the AIM bridge; and
   (b) **A14/W7/W10** (knower-known-knowing collapses in the Subject, is tripartite in
   the conditioned) is core witness-centered content missing from §4 and should be
   modeled.
3. **Naming of the public API** (`Interaction`/`Claim`/`classify`) — confirmed
   idiomatic; final reconciliation with AIM's conventions deferred to Task 2.

*New for user ruling:* item 2(a) — adopt the Ego cluster into Tier 1 of the bridge?
And note (catalogue §5.4) that **M8** now gives axiom backing for "adhyāsa never
changes the Self" (the *asaṅga* principle), and **W9/M17** give a structural correlate
for "liberating knowledge removes ignorance" even though experiential *mokṣa* stays
out of scope (§11(4)).

---

## 13. Deliverables checklist (Task 1)

- [x] Design document — language, representation, API, with reasoning *(this file)*
- [x] Module 1: sorts / ontology / levels — 9/9 tests pass
- [x] Engine + report: Interaction / Claim / check() / classify() — 9/9 tests pass
- [x] Axiom modules (Sonnet): core, levels, maya, jiva/isvara, awareness, additional, temporal, event — 27/27 tests pass
- [x] Axiom module: state.py (AV-series + *ānandamaya* §17.2(3) border-flag, ruling b) — 11/11 tests pass
- [x] Implemented library with all core constructs (§4–6) — 56/56 tests pass
- [x] Developer docs usable without Advaita background — `scherf/README.md`
- [x] Demonstration — `demo.py` (four scenarios, including the §8 behaviorist-failure case)
- [x] §17.2 limits assessment and handling — `docs/limits.md`

---

## 14. Summary of decisions for your confirmation

1. **Language:** Python 3.11+, stdlib-only core. *(Confirmed.)*
2. **Representation:** transparent object + named-rule checker; Z3 deferred behind the
   same interface. *(Confirmed.)*
3. **`Y` as an immutable constant** — the witness-centered commitment enforced by the
   type system, not by policy. *(Confirmed.)*
4. **API:** `Interaction.assert_claim` → `check()` (legible report) → `classify()`
   (three-level epistemics). *(Confirmed — idiomatic Python; final naming to be
   reconciled with AIM's own conventions when AIM is cloned in Task 2, so the
   `import scherf` call site in AIM reads naturally.)*
5. **Two-tier AIM bridge** with the two rulings and the stage/qualification boundary.
   *(Confirmed.)*
6. **Limits handled by explicit non-representation markers**, never silent
   approximation. *(Confirmed.)*

**All §14 decisions confirmed (2026-05-31).** Implementation proceeds module-by-module
following §5, encoding against the cloned `AdvaitaVedanta/*.lean` source per the open
fidelity item in §12.1.
