# Reconciled Axiom Catalogue — Scherf *Advaita* Lean Formalization

*The authoritative source of truth for implementing the Scherf library (Task 1).
Reconciled directly from the cloned `AdvaitaVedanta/*.lean` files (Step 0,
2026-05-31), NOT from the repository README.*

> **Why this document exists.** The *old* README presented a *representative subset*
> and named "69 axioms." The actual Lean source contains substantially more — both
> extra predicates and several whole axiom series the old README omitted. The design
> doc (§12.1) committed to encoding against the `.lean` source. This catalogue is that
> source, transcribed and organized for implementation.
>
> **UPDATE 2026-05-31 (eve):** Scherf re-uploaded the README (now **v5.0.0**). The new
> README is a complete, accurate spec that **matches this catalogue** and openly states
> **129 primitive axioms across ten modules**, with a per-series count table (§16) that
> equals our reconciliation exactly (A=15, K=8, M=16, J=6, I=5, U=4, S=6, G=3, CA=2,
> EG=3, ST=5, CH=4, W=10, T=6, E=10, AV=23, State-distinct=3). The `.lean` source did
> **not** change (last modified 2025-12-25). The limits section moved to README §17.2
> (the briefing called it §13.2). **Net effect: this catalogue and the design doc are
> validated, not invalidated.** Lean pinned to v4.12.0.

---

## 0. Headline findings (what changed vs. the README / design-doc §4)

1. **The "69" is conceptual, not a literal axiom count.** Counting Lean `axiom`
   declarations (with sub-lettered axioms like `A1a`/`A1b` as one conceptual axiom)
   the source has well over 100 declarations across 11 modules. Many README axioms are
   actually *derived theorems* in the source (marked "NOTE: … removed/derivable"). The
   library encodes the **stated axioms**, and may optionally encode the derived
   theorems as convenience checks.
2. **Whole series the README omitted are present and relevant:**
   - **W-series (W2–W11)** — Awareness/witness axioms, incl. the knower-known-knowing
     structure. *Central to witness-centered design.*
   - **EG-series (EG1, EG2, EG4)** — the **Ego** axioms (`Ego`, `ApparentSubject`,
     `Identifies`). *This is a direct formal model of the profiling/misidentification
     mechanism — see §6 finding.*
   - **ST-series (ST1–ST5, spacetime)** — `SpaceItself`/`TimeItself` as conditioned.
   - **CA-series (CA1, CA4)** — causation between events.
   - **CH-series (CH1–CH4)** — change/birth/death of the Absolute vs. conditioned.
3. **The extra predicates flagged as open items in §12.2 are all real and load-bearing:**
   `Ego`, `ApparentSubject`, `Identifies`, `Knower`/`Known`/`Knowing`,
   `DistinctAspects`, `Knowledge`, `Liberating`, `Possesses`, `SpaceItself`,
   `TimeItself`, `Body`, `Embodied`, `Layer`, `RealChange`, `Changes`, `Born`, `Dies`,
   `Remembers`, `StateTransition`, `MayaLevel`.
4. **The user's *ānandamaya*/causal-body ruling is corroborated by the source:** AV15
   says in *suṣupti* "only the causal body (seed of ignorance) persists" — i.e.
   `KaranaSarira` is the seed of *avidyā*. This directly supports treating the
   *ānandamaya* superimposition as the root/*mūlāvidyā*-bordering case (design-doc §9, ruling (b)).

---

## 1. Module map (11 files under `AdvaitaVedanta/`)

| Lean file | Series | Encodes |
|---|---|---|
| `Signature.lean` | — | sorts, constants, all predicate declarations, state-distinctness axioms |
| `CoreAxioms.lean` | A (+ derived) | identity, partition, grounding, witness, knower-trinity |
| `LevelAxioms.lean` | K | three levels, sublation hierarchy |
| `MayaAxioms.lean` | M | *adhyāsa*, *vivarta*, *avidyā*, *bādha* |
| `JivaIsvara.lean` | J, I | individual & cosmic subject |
| `AwarenessAxioms.lean` | W | perception vs. witnessing, knowledge structure |
| `AdditionalAxioms.lean` | U, CA, S, G, EG, ST, CH | upādhi, causation, sheaths, guṇas, **ego**, spacetime, change |
| `StateAxioms.lean` | AV | *avasthā-traya*, witness/*turīya*, reality criterion |
| `TemporalAxioms.lean` | T | time ordering |
| `EventAxioms.lean` | E | events, occurrence, causation |
| `Theorems.lean` | — | master theorems (Tat Tvam Asi, three-state analysis) |

---

## 2. Sorts, constants, predicates (`Signature.lean`)

**Sorts (5):** `Obj`, `Level`, `Time`, `Event`, `State`.
**Level constants:** `Param`, `Vyav`, `Prat`.
**State constants:** `Jagrat`, `Svapna`, `Susupti` (+ pairwise-distinctness axioms
`State_distinct_JS/SSu/JSu`). *turīya is NOT a State constant — it is `Y`'s
transcendence (AV18).*

**Predicate inventory** (grouped; ★ = absent from design-doc §4, add it):

- **Core nature:** `A`, `C`, `Y`; `T_p`, `S_p`, `Q_p` (+ def `Phi`); `Sat`, `Cit`,
  `Ananda` (+ def `Saccidananda`).
- **Ontological relations:** `Level_of`, `Cond`, `MayaPow`, ★`MayaLevel`,
  `Superimposed`, `Appears`, `IgnoranceOf`, `Upadhi`, `Sublates`.
- **Entity classes:** `Jiva`, `Isvara`, `World`; `SthulaSarira`, `SukshmaSarira`,
  `KaranaSarira` (śarīra-traya); ★`Body`, ★`Embodied`.
- **Awareness:** `Perceives`, `Witnesses`, ★`Possesses`; ★`Knower`, ★`Known`,
  ★`Knowing`, ★`DistinctAspects`, ★`Knowledge`, ★`Liberating`.
- **States:** `InState`, `Manifests`, ★`StateTransition`, ★`Remembers`.
- **Change:** ★`RealChange`, ★`Changes`, ★`Born`, ★`Dies`.
- **Sheaths:** `Annamaya`, `Pranamaya`, `Manomaya`, `Vijnanamaya`, `Anandamaya`
  (+ def `Sheath`); ★`Layer`.
- **Guṇas:** `Sattva`, `Rajas`, `Tamas` (+ def `HasGuna`).
- **Ego & spacetime:** ★`Ego`, ★`ApparentSubject`, ★`Identifies`, ★`SpaceItself`,
  ★`TimeItself`.
- **Events:** ★`EE`, `Before`, `OccursAt`, `EventOf`, `CausesEvent`; constructors
  ★`PerceptionEvent`, ★`ChangeEvent`, ★`BirthEvent`, ★`DeathEvent`.

---

## 3. Axioms by series (stated axioms only; derived theorems noted)

### A — Core (`CoreAxioms.lean`)
- **A1a** every entity is `A` ∨ `C`; **A1b** not both (exhaustive exclusive partition).
- **A2** exactly one Absolute. **A3** exactly one Subject `Y`.
- **A4** `Y x ↔ A x` (*Tat Tvam Asi*).
- **A5** Absolute self-grounds (`Cond a a`). **A6** everything grounded in some Absolute.
- **A7a** Absolute ¬temporal ∧ ¬spatial ∧ ¬qualitative. **A7b** Absolute is `Saccidananda`.
- **A8** Conditioned ⇒ `Phi` (phenomenal). **A9** mutual grounding ⇒ identity ∧ Absolute.
- **A10** grounding transitive. **A11** Absolute witnesses everything.
- **A13** `Y u → ¬Perceives u o` (Subject never perceives dualistically).
- **A14** `Y u → Knower u ∧ Known u ∧ Knowing u` (collapsed knower-trinity). ★ *new to our model.*
- *Derived:* A2b, A3b, A7 (¬Phi), A12 (self-witnessing).

### K — Levels (`LevelAxioms.lean`)
- **K1** every entity at Param ∨ Vyav ∨ Prat. **K2/K2a/K2b** Absolute at Param only.
- **K3** Conditioned ¬at Param. **K4** Conditioned at Vyav ∨ Prat.
- **K5** `C x ∧ Level_of x Vyav ∧ Level_of y Prat → Sublates x y` (hierarchical sublation).
- **K6** Vyav non-empty.

### M — Māyā (`MayaAxioms.lean`)
- **M1** `MayaPow a x → A a`. **M2** Conditioned arises via some Absolute's māyā.
- **M3** māyā operates at Vyav & Prat, not Param. **M4** `MayaPow a x → Cond a x`.
- **M5** Absolute not subject to māyā.
- **M6** `Superimposed x y → C x` (superimposed thing is conditioned).
- **M7** `Superimposed x y → A y` (**substrate is the Absolute**).
- **M8** `Superimposed x y → Appears x y ∧ ¬RealChange y x` (**substrate undergoes no real change** — the *asaṅga* principle, formalized).
- **M9** `Appears x y → ¬RealChange x y` (*vivarta*). **M10** Conditioned appears on some Absolute.
- **M12** `IgnoranceOf s x → A x` (ignorance is always *of* the Absolute).
- **M13** ignorance + superimposition ⇒ a relation between knower and superimposed.
- **M15** Absolute has no ignorance.
- **M16** sublation relates two `Knowledge`s. **M17** Liberating knowledge sublates empirical knowledge. **M18** sublation asymmetric.
- *Removed/derived:* M11 (from A7b), M14 (= J6).

### J / I — Jīva & Īśvara (`JivaIsvara.lean`)
- **J1** Jīva is `C`. **J2** Jīva at Vyav. **J4** Jīva embodied. **J6** Jīva has ignorance of some Absolute. **J7a** Jīva has spatial upādhi. **J8** ≥2 distinct jīvas.
- **I1** Īśvara is `C`. **I2** Īśvara at Vyav. **I4** Īśvara has omniscient quality (`Q_p`). **I5** unique Īśvara. **I6** Īśvara related to all Vyav.
- *Derived:* J3, J5, J9, J10, I3.

### W — Awareness (`AwarenessAxioms.lean`)
- **W2** witnessing is not an event (timeless). **W3** perception produces a temporal event.
- **W4** perceiver is conditioned. **W5** witnessing another ⇒ `Y`. **W6** perception requires subject≠object.
- **W7** `Y u → ` knower/known/knowing collapse into `u`. **W8** conditioned knowledge is tripartite (distinct k/n/g).
- **W9** `Liberating k ∧ Jiva j ∧ A a → (Possesses j k → ¬IgnoranceOf j a)` (**liberating knowledge removes ignorance**).
- **W10** Subject transcends the tripartite structure. **W11** whatever witnesses everything is the Absolute.
- *Derived:* W1 (Y witnesses all, from A4+A11).

### U / CA / S / G / EG / ST / CH (`AdditionalAxioms.lean`)
- **U1** `Upadhi u x → C x`. **U2** Absolute has no upādhi. **U3** distinct jīvas share a space-upādhi. **U4** upādhi distinguishes conditioned from its grounding Absolute.
- **CA1** causation relates two Vyav events. **CA4** causation transitive. *(CA2=E10, CA3=E9 removed.)*
- **S1** Sheath ⇒ `C`. **S3–S6** layering Annamaya→Pranamaya→Manomaya→Vijnanamaya→**Anandamaya**. **S7** `Layer x y → Cond y x`. *(S2, S8 derived.)*
- **G1** Conditioned has guṇa. **G2** Absolute transcends the three guṇas. **G3** Vyav conditioned changes under guṇas.
- **EG1** `Ego e → C e`. **EG2** `Ego e → ∃ s b, ApparentSubject s ∧ Body b ∧ Identifies s b` (**ego = an apparent subject identifying with a body**). **EG4** removing ignorance removes ego. *(EG3 derived; T28: "ego is fiction.")*
- **ST1–ST5** `SpaceItself`/`TimeItself` are conditioned, at Vyav, and sublated by liberating knowledge.
- **CH1** Absolute ¬changes. **CH2** ¬born. **CH3** ¬dies. **CH4** Vyav conditioned is born/dies/changes.

### AV — States (`StateAxioms.lean`)
- **AV1a/b** every jīva in exactly one state. **AV2** the state-transition cycle.
- **AV3a/b, AV4** waking: gross body, world, and subtle body manifest. **AV5** waking world objects at Vyav.
- **AV6, AV7** dream: gross body & external world do not manifest. **AV8** subtle body active. **AV9** dream objects are mind-dependent. **AV10** dream objects at Prat.
- **AV11** deep sleep: nothing manifests. **AV15** only the **causal body (seed of ignorance)** persists in *suṣupti*. ★ *corroborates the ānandamaya ruling.*
- **AV16** witness persists through all states. **AV18** witness never in any state (*turīya*).
- **AV20** waking remembers having slept. **AV22** what appears in one state but not another is ¬Absolute (reality criterion). **AV23** Absolute never empirically manifests.
- **AV24a/b/c** the three bodies are conditioned. **AV25** world entities conditioned.
- *Derived:* AV12, AV13, AV14, AV17, AV19, AV21; plus the ST1–ST15 *theorems* and the "You are not the body/mind/world" corollaries.

### T — Temporal (`TemporalAxioms.lean`)
- **T1** irreflexive. **T2** transitive. **T3** asymmetric. **T4** linear. **T5** time non-empty. **T6** distinct times exist.

### E — Event (`EventAxioms.lean`)
- **E1** event exists ↔ occurs at some time. **E2** unique occurrence time. **E3** event has an object. **E4** event-object grounding. **E5–E8** event constructors (perception/change/birth/death). **E9** causal ordering ⇒ temporal precedence. **E10** Absolute has no events.

---

## 4. Key theorems (`Theorems.lean`, `StateAxioms.lean`) — for the demo & tests

`Brahman := choose A2.1`, `Atman := choose A3.1`.
- **T0** `Brahman = Atman`. **T5** `Y u ↔ A u`. **T7** ontological monism at Param.
- **T13** Absolute transcends phenomenality. **T14** "you witness all." **T19** "subject does not perceive." **T22** "you are knower-known-knowing."
- **T27** sheaths ≠ Self. **T28** "ego is fiction." **T29** Self transcends guṇas. **T37** `Ananda Atman`.
- **MasterTheorem_TatTvamAsi** and **MasterTheorem_ThreeStateAnalysis** — the two capstones; good acceptance targets for the library's worked example (§8 of the design doc).

These are **already machine-verified in Lean** — the library must not re-prove them; it
may encode them as named consistency checks / regression tests against the object model.

---

## 5. Design implications for the library (feeds back into the design doc)

1. **Add the Ego cluster to the bridge (recommended, philosophical — for user ruling).**
   `EG1/EG2/T28` give a *precise* formal model of the profiling/misidentification
   mechanism: an `Ego` is a conditioned `ApparentSubject` that `Identifies` with a
   `Body`. This is sharper than `Superimposed(C, A)` alone. **Profiling the user ≈
   constructing an `Ego`/`ApparentSubject` that identifies the user with a
   body/profile (EG2) — a conditioned fiction (EG1, T28).** Recommend elevating this
   to Tier 1 of the AIM bridge alongside `Superimposed`.
2. **`adhyāsa` never touches the Self is now axiom-backed.** M8 (`¬RealChange y x` on
   the substrate) formally encodes the *asaṅga* principle the user confirmed — cite M8
   in the library's `Superimposed` check and in §1 of the design doc.
3. **Knower-Known-Knowing (A14/W7/W8/W10) must be modeled.** The collapse-in-the-Subject
   vs. tripartite-in-the-conditioned distinction is core witness-centered content and
   was missing from design-doc §4.
4. **Liberating knowledge has a structural correlate (W9, M17, ST5) even though
   experiential *mokṣa* is out of scope.** Distinction to preserve: the library *can*
   check "liberating knowledge removes ignorance / sublates empirical knowledge"
   (a relation among `Knowledge`/`IgnoranceOf`), but does *not* model *mokṣa* as a
   produced state (design-doc §11(4)). Worth a sentence in §11.
5. **Module layout (design-doc §5) maps cleanly** onto the 11 Lean files; add an
   `axioms/awareness.py` (W), fold Ego/spacetime/change into `axioms/additional.py`
   (or split), matching `AdditionalAxioms.lean`.

---

*Source: github.com/matthew-scherf/Advaita, cloned to /tmp/Advaita on 2026-05-31
(re-clone as needed; /tmp is ephemeral). Transcribed from the `.lean` files, not the README.*
