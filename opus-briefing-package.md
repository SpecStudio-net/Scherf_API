# Briefing Package for Claude Opus 4.8
## Witness-Centered Software: Three Engineering Tasks

*Prepared by Dev Bhagavān / SpecStudio*

---

## Who You Are Working With

I am a software architect and contemplative practitioner. I have spent decades
studying *Advaita Vedānta* and related Eastern philosophical traditions in their
native cultural contexts, and I have been a software engineer and tech writer on and off since the late 1970s. I
am now building AI systems grounded in Advaita's model of consciousness rather
than the behaviorist premise that dominates current AI design. I work in
VS Code with Claude Code. I am not deeply familiar with current language ecosystems
and will rely on your judgment for implementation decisions.

---

## Background: What Witness-Centered Design Is

Most AI interaction systems are built on an implicit behaviorist model of the
human being: the user is a bundle of preferences, behaviors, and measurable
responses to be modeled and optimized. This produces real and documented failure
modes — cognitive dependency, learning atrophy, the erosion of independent
judgment, and what is increasingly called "AI psychosis."

Witness-centered design is an alternative architectural approach grounded in
*Advaita Vedānta's* model of the conscious subject. The central principle: the
user is not reducible to their preferences or behavioral profile. They are the
*sākṣin* — the witness-consciousness — the knowing subject in which all experience,
including their interaction with the AI system, appears. A system designed to
serve this knowing subject looks and behaves differently from a system designed
to optimize for behavioral outcomes.

The practical consequences: a witness-centered system preserves the user's
orientation and cognitive independence, presents its outputs with appropriate
epistemic humility (distinguishing levels of certainty), supports the user's
own understanding rather than substituting for it, and refuses to profile or
manipulate. These are architectural principles, not policy overlays.

---

## The Formal Foundation: Scherf's Advaita Formalization

Matthew Scherf has formalized *Advaita Vedānta* in Lean 4 — the first
machine-verified formalization of a non-western philosophical system. The system
comprises 69 axioms across ten modules:

- **Core metaphysics** (A-series): the identity of *Ātman* and Brahman, exhaustive
  partition of entities into Absolute and Conditioned
- **Level axioms** (K-series): three ontological levels — *prātibhāsika* (illusory),
  *vyāvahārika* (conventional), and *pāramārthika* (ultimate)
- ***Māyā* axioms** (M-series): superimposition (*adhyāsa*), appearance (*vivarta*),
  ignorance (*avidyā*)
- ***Jīva/Īśvara* axioms** (J/I-series): the individual and cosmic subject
- ***Upādhi/Guṇa* axioms** (U/G-series): limiting adjuncts, the three qualities
- **Sheath axioms** (S-series): the five sheaths (*pañca-kośa*)
- **Temporal and Event axioms** (T/E-series): formal time and causation structure
- **State axioms** (AV-series): the three-state analysis (*avasthā-traya*) —
  waking (*jāgrat*), dream (*svapna*), deep sleep (*suṣupti*) — and the
  witness (*sākṣin*) that persists through all three

All proofs are machine-verified. The system is logically consistent.

**Repository:** https://github.com/matthew-scherf/Advaita

The README contains the full formal specification including all axioms, theorems,
and Lean 4 definitions. Read it in full before beginning Task 1.

---

## The Special/General Theory Framework

There are three tasks, sequential and interdependent:

**Task 1 — Build the Scherf library.** The General Theory first: Scherf's axiom system
encoded as a software library providing a domain-agnostic model of the sentient user,
usable as a foundation for any AI application. This is the formal yardstick against
which everything else will be measured.

**Task 2 — Audit and refactor AIM.** The Special Theory: a domain-specific application
of witness-centered design to *Advaita Vedānta* pedagogy. Built and working, but
vibe-coded and requiring systematic audit and correction — now guided by the formal
library rather than judgment alone.

**Task 3 — Validate AIM using the library.** With both in hand, use the General
Theory library to validate the Special Theory's implementation — confirming that AIM's
diagnostic logic, state machine, and *prakriyā* selection correctly implement the
*Advaita* model across its full spectrum of use cases.

The tasks must proceed in order: the library must exist before AIM can be audited
against it, and AIM must be audited and corrected before validation can be meaningful.

---

## Task 1: The General Theory — Encoding Scherf's Axioms

### The Goal

Encode Scherf's 69-axiom formal system as a software library providing a
domain-agnostic model of the sentient user. This library should be usable by
any AI application developer as a formal foundation — replacing the implicit
behaviorist premise with an explicit, examined model of what a conscious human
being is.

The library is not an AI system. It is a formal model — a set of constructs,
constraints, and query interfaces derived directly from Scherf's axiom system —
that AI systems can use to reason about their users correctly. It is also the
formal yardstick against which AIM will be audited and validated in Tasks 2 and 3.

### Design Decisions to Make First

Before writing code, produce a design document addressing:

1. **Implementation language.** Consider Python (largest developer reach, natural
   fit with the existing AIM codebase), TypeScript (natural fit for web-based AI
   applications), or a language-agnostic specification with reference implementations.
   Make a recommendation with reasoning.

2. **Representation of the axiom system.** Scherf's axioms are first-order logic.
   How should they be represented in software? Options include: direct logical
   encoding using a Python logic library; an object model representing the ontological
   entities (Obj, Level, State, etc.) and their relationships; a constraint system
   that can evaluate whether a given interaction state satisfies the axioms; or a
   hybrid approach. Make a recommendation.

3. **The API surface.** What does an application developer actually call? The
   library needs to be usable by someone who understands AI application development
   but not necessarily *Advaita Vedānta*. Design the API to be intuitive at the
   application level while being formally grounded in the axiom system. Key
   questions: how does the developer register a user interaction? How do they
   query whether a proposed system response is consistent with witness-centered
   principles? How do they access the three-level framework for epistemic
   classification of outputs?

4. **The relationship to AIM.** The General Theory library, once built, should
   be importable by AIM. The AIM teaching engine's *prakriyā* selection and diagnostic
   logic should be expressible in terms of the General Theory's constructs. Design
   the library with this downstream use in mind.

### Core Constructs to Implement

Working from Scherf's axiom system, the library must represent at minimum:

- The fundamental partition: Absolute (A) and Conditioned (C), mutually exclusive
  and exhaustive
- The three ontological levels: *Prat* (prātibhāsika), *Vyav* (vyāvahārika),
  *Param* (pāramārthika) — with the level assignment predicate and hierarchical
  sublation relation
- The witness-consciousness (*sākṣin*): the unique Subject (Y), its identity
  with the Absolute (Axiom A4: *Tat Tvam Asi*), and the key theorems (it witnesses
  everything, it is never in any state, it never perceives dualistically)
- The superimposition (*adhyāsa*) relation: the mechanism by which conditioned
  entities are mistakenly identified with the Absolute — the central diagnostic
  category for witness-centered design
- The three states (*avasthā-traya*): *Jagrat*, *Svapna*, *Suṣupti*, with the
  witness persisting across all three (Axiom AV16) and transcending them (AV18)
- The criterion of reality (AV22): what appears in one state but not another
  cannot be ultimately real — the basis for epistemic level classification of
  system outputs

### Deliverables for Task 1

- A design document covering language choice, representation approach, and API
  design, with reasoning for each decision
- The implemented library, with all core constructs from Scherf's axiom system
- Documentation sufficient for a developer unfamiliar with *Advaita Vedānta* to
  use the library effectively
- A demonstration of the library being used to evaluate a sample AI interaction
  against witness-centered principles
- An assessment of what Scherf's axiom system cannot yet represent in software
  (corresponding to his own Section 13.2 on the limits of the formalization) and
  how the library should handle these limits

---

## Task 2: AIM Audit and Correction

### What AIM Is

The Advaita Inquiry Matrix is a structured AI-assisted pedagogical system designed
to model and reproduce the teaching logic of the *Advaita Vedānta* tradition. Although it presents a chat interface to the user, it is
not a general-purpose chatbot. Its purpose is to diagnose a student's current
conceptual errors (*adhyāsa*), select the appropriate classical teaching method
(*prakriyā*), route to relevant scriptural passages, and conduct structured
philosophical dialogue — guiding the student toward recognition of the *sākṣin*.

The architecture mirrors the traditional *guru–śiṣya* structure:

| Traditional | AIM Layer |
|---|---|
| *Śruti* (scripture) | corpus/ |
| *Prakriyā* (teaching method) | pedagogy/ |
| *Guru* reasoning | teaching_engine/ (engine/) |
| *Śiṣya* cognition | system/state_machine/ |
| Teaching dialogue | system/dialogue_protocols/ |

The inquiry flow: student input → error detection → student state assessment →
*prakriyā* selection → scripture routing → dialogue generation.

**Repository:** https://github.com/SpecStudio-net/Advaita-Inquiry-Matrix

**Language:** Python throughout.

**Current status:** Basic development complete, in tuning stage. Built primarily
through vibe-coding — conceptually grounded, but likely containing implementation
errors, gaps between intent and behaviour, and missing test coverage.

### What the Audit Should Cover

Begin by reading the full codebase — README.md, PROJECT_OVERVIEW.md,
AIM_directory_map.txt, and all source files. The Scherf library (Task 1) is now
the formal reference — use it to inform your assessment throughout. Then evaluate:

1. **Architectural integrity.** Does the actual implementation match the
   documented architecture? Are separation-of-concerns boundaries maintained?
   Does runtime code reference the corpus directly, or only through the teaching
   engine?

2. **Pedagogical correctness.** The *prakriyā* selection logic is the core of the
   system. Does it correctly implement classical Advaita teaching methods? Are the
   diagnostic categories (types of *adhyāsa*, student cognitive states) complete
   and correctly defined? Are the mappings from diagnostic category to *prakriyā*
   to scriptural passage coherent?

3. **State machine completeness.** Does the student state model cover the full
   range of cognitive states the tradition addresses? Are there missing states,
   incorrect transitions, or states that cannot be reached by the current logic?

4. **Implementation errors.** Vibe-coded Python accumulates specific categories
   of error: inconsistent variable naming, missing edge case handling, incorrect
   assumptions about data structure, logic errors in conditional branches, silent
   failures. Identify and correct these throughout.

5. **Test coverage.** The existing test_engine.py and eval_signal_haiku.py files
   represent the beginning of a test suite. Expand this into comprehensive coverage
   of the teaching engine's intended behaviour — including edge cases, unusual
   student states, and failure modes.

6. **Documentation gaps.** Identify any files or modules whose purpose and
   behaviour is unclear from the existing documentation, and add appropriate
   docstrings and comments.

### Deliverables for Task 2

- A written audit report identifying all significant issues found, organized by
  category (architectural, pedagogical, implementation, testing)
- Corrected source files for all issues identified
- An expanded test suite with reasonable coverage of the teaching engine's
  intended behaviour
- A brief assessment of the system's current pedagogical accuracy and the gaps
  that remain

---

## Task 3: Validating AIM Against the Library

### The Goal

With the Scherf library built (Task 1) and AIM audited and corrected (Task 2),
use the library as a formal yardstick to validate AIM's correct operation across
its full spectrum of use cases. This is the payoff of the Special/General Theory
framework: the General Theory makes rigorous validation of the Special Theory
possible for the first time.

### What Validation Covers

1. **Diagnostic logic.** Does AIM's *adhyāsa* detection correctly identify the
   forms of misidentification that Scherf's axiom system defines? Are there
   diagnostic categories in the library that AIM does not handle, or handles
   incorrectly?

2. **State machine coverage.** Does the student state machine cover the full
   range of cognitive states that the *avasthā-traya* and *sākṣin* framework
   implies? Are all reachable library states reachable in AIM?

3. **Prakriyā selection.** Does each *prakriyā* in AIM's pedagogy layer
   correspond correctly to the library's model of what is needed at each
   diagnostic state? Are there cases where the library would prescribe a
   different response than AIM currently produces?

4. **Epistemic level classification.** Do AIM's dialogue outputs correctly
   observe the distinction between *prātibhāsika*, *vyāvahārika*, and
   *pāramārthika* claims, as the library defines them?

5. **Edge cases and failure modes.** Drive AIM through the full range of inputs
   implied by the library's state space — including unusual student states,
   boundary conditions, and combinations not encountered in normal single-practitioner
   use — and document any failures.

### Deliverables for Task 3

- A validation report mapping AIM's behaviour against the library's formal model,
  organized by the categories above
- Corrected AIM source files for any failures identified during validation
- An updated assessment of AIM's pedagogical accuracy, now expressed in terms of
  the formal library rather than judgment alone
- A summary of any gaps in the library itself that the validation process exposes

---

## Working Principles

A few principles to maintain throughout both tasks:

**Sanskrit terms** should be preserved and used correctly. The library and its
documentation should use the proper IAST-transliterated terms (*sākṣin*, *adhyāsa*,
*pāramārthika*, etc.) alongside plain-language explanations, not replaced with
approximations.

**Conceptual fidelity** takes priority over implementation convenience. If a clean
implementation requires simplifying the Advaita model in a way that loses
something philosophically important, flag it and discuss rather than proceeding
silently.

**The user (me) is not a Python expert.** Explain significant design decisions
in terms of their consequences and tradeoffs, not just their technical details.
I will be maintaining this code.

**Raise questions.** All three tasks involve design decisions that have philosophical
as well as technical implications. Flag these as they arise rather than resolving
them unilaterally.

---

## Where to Start

Read this document fully. Then:

1. Read the AIM README and PROJECT_OVERVIEW.md at the repository above.
2. Read the full Scherf formalization README at his repository above.
3. Clone the AIM repository and read the full codebase.
4. Produce an initial assessment: what you understand AIM to be doing, what
   the Scherf system provides, your preliminary thinking on the design decisions
   for Task 1, and how you propose to structure the Task 3 validation.
5. Confirm your understanding with me before beginning implementation.

The three tasks must proceed in sequence. Do not begin Task 2 until Task 1 is
complete and confirmed. Do not begin Task 3 until Task 2 is complete and confirmed.

---

*Contact: Dev Bhagavān, SpecStudio — hello@specstudio.net*
