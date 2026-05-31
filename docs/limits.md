# Formalization Limits and How the Library Handles Them

*Task 1 deliverable — the §17.2 assessment (design doc §11).*

Matthew Scherf's README (v5.0.0 §17.2) names four things that classical first-order
logic cannot fully capture. This document records each limit, states the library's
policy for handling it, and where relevant notes what the library *can* still do at
the structural level even though it cannot model the full philosophical content.

The governing principle (design doc §11): wherever the formalism stops, the library
**says so explicitly** — via a documented "not modeled" boundary or a
`Violation.borders_limit` marker — so an application never mistakes silence for a
clean result.

---

## §17.2(1) — Māyā's indeterminacy (*sadasadvilakṣaṇa*)

**The limit.** Māyā is classically described as "neither real nor unreal" — it
transcends the binary that classical logic provides. A formal system built on
true/false predicates cannot express this indeterminate ontological status.

**What the library models.** `Superimposed` and `Appears` (*vivarta*) are modeled as
first-class predicates. M6/M7 check that superimposition is always of a conditioned
thing upon the Absolute; M8 confirms the substrate is unchanged. This covers the
*mechanism* of māyā (how superimposition works and what its effects are).

**What the library does not model.** The *ontological status of māyā itself* — whether
māyā is ultimately real, ultimately unreal, or neither — is not represented as a
boolean. There is no `is_maya_real()` function that returns `True` or `False`. This
gap is left explicit: applications that need to discuss māyā's ontological status
should document that they are operating within the classical-logic approximation.

---

## §17.2(2) — The performative dimension of *Tat Tvam Asi*

**The limit.** "Tat Tvam Asi" (That thou art) is not merely a proposition to be
evaluated as true or false. It is a *mahāvākya* — a great saying whose utterance in
the right context is meant to trigger direct recognition (*aparokṣa-anubhūti*) in the
student. Classical FOL models the propositional content but not this performative/
recognitional event.

**What the library models.** The proposition `Y ↔ A` (axiom A4) is encoded and
enforced: any entity classified as the Subject is identical with the Absolute, and
vice versa. The derived theorem T0 (Brahman = Ātman) follows from A2/A3/A4 and is
available as a consistency check.

**What the library does not model.** The event of recognition itself — the shift from
intellectual understanding to direct seeing — is out of scope by nature. It is not a
logical inference; it is not a state the library can represent. This is also why
*mokṣa* (§17.2(4) below) is not modeled as a produced state.

---

## §17.2(3) — Beginninglessness of *avidyā* (*anādi*)

**The limit.** Advaita holds that ignorance (*avidyā*) is *anādi* — without beginning.
This requires modal or non-well-founded logical frameworks that classical FOL does not
support. The formalization cannot assert that `IgnoranceOf(jīva, Absolute)` has no
temporal origin.

**What the library models.** `IgnoranceOf` is a predicate (M12: ignorance is always of
the Absolute; J6: every jīva has it). Its presence or absence can be checked. W9
models that possessing liberating knowledge removes it. The library deliberately does
not assert a temporal origin for `IgnoranceOf` — it is modeled as a structural fact
about the jīva, not as something that began at a time.

**Where the border-flag applies.** The *ānandamaya* (bliss-sheath) superimposition
borders this limit. AV15 identifies the causal body (*kāraṇa-śarīra*), with which
*ānandamaya* is associated, as the seed of ignorance persisting in deep sleep. Śaṅkara's
reading of *ānandamayo'bhyāsāt* (Brahma Sūtra) establishes that *ānandamaya* is not
Brahman but a kośa rooted in *avidyā*. Superimposing it therefore shades into
*mūlāvidyā* — the root ignorance whose beginninglessness is the classical doctrine.

**Library policy for the *ānandamaya* case.**
`check_sheath_superimposition(Sheath.ANANDAMAYA, SELF)` runs the *same*
`Superimposed(Ānandamaya, Y)` structural check as the other four sheaths, but returns
a `Violation` with `borders_limit = "§17.2(3) — anādi-avidyā (mūlāvidyā: the
beginninglessness of ignorance)"`. This means:

- The structural diagnosis is still made — identifying with the bliss-sheath *is*
  *adhyāsa*, and the library correctly flags it.
- The result is marked as a **root case**, not one of five equals, so an application
  (or AIM) treats it with appropriate depth rather than routing it as an ordinary
  sheath-error.
- The marker is never silent: `str(violation)` renders the ⚠ note explicitly.

---

## §17.2(4) — Liberation as recognition, not a produced state

**The limit.** *Mokṣa* is not the production of a new state — it is the recognition of
what was always the case. Classical logic can model propositions and states; it cannot
model the event of recognition.

**What the library does not model.** There is no `liberated` state, no `moksa_achieved`
flag, and no transition function from ignorance to liberation. *Viṣaya-adhyāsa-mokṣa*
is out of scope by design (see design doc §9, ruling 2).

**What the library can still check.** The *structural* correlates of the path are
modeled:
- W9: possessing liberating knowledge (`Liberating(k)`) removes ignorance
  (`¬IgnoranceOf(j, a)`).
- M17: liberating knowledge sublates empirical knowledge.
- ST5: liberating knowledge sublates space-knowledge and time-knowledge.
- EG4: removing ignorance dissolves the ego.

These let an application (or AIM) check that a pedagogical sequence is structurally
consistent — that knowledge claimed to be liberating has the right properties — without
modeling the recognitional event itself. The distinction is between "this knowledge has
the right structure to be liberating" (checkable) and "recognition occurred"
(not checkable).

---

## Summary table

| Limit | Library policy | Marker / mechanism |
|-------|---------------|-------------------|
| §17.2(1) Māyā indeterminacy | Mechanism modeled (Superimposed/Appears/M6–M9); ontological status of māyā not represented | Documented "not modeled" |
| §17.2(2) Performative *mahāvākya* | Proposition A4 (`Y ↔ A`) modeled; recognitional event not in scope | Documented "not modeled" |
| §17.2(3) *Anādi avidyā* | IgnoranceOf modeled as structural fact; no temporal origin asserted; *ānandamaya* case carries border-flag | `Violation.borders_limit` on Sheath.ANANDAMAYA |
| §17.2(4) *Mokṣa* as recognition | Structural correlates (W9/M17/ST5/EG4) modeled; *mokṣa* as produced state not in scope | Documented "not modeled" |

---

*Source: Scherf, M., Advaita Vedānta Formal Specification, README v5.0.0 §17.2.
Library: `scherf/` (Task 1). Design rationale: `docs/task1-design.md` §11.*
