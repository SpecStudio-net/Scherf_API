"""AV-series axiom checks — the three-state analysis (*avasthā-traya*).

Source: ``StateAxioms.lean`` (AV1–AV25, minus the derived AV12/13/14/17/19/21).

This module also houses the **sheath superimposition** check — the formal core of the
AIM bridge's diagnostic (design doc §9). Identifying the user with one of the five
sheaths (*pañca-kośa*) is ``Superimposed(kośa, Y)``: an *adhyāsa* whose substrate is
the witness.

The *ānandamaya* (bliss-sheath) case is special, per your ruling (b) (2026-05-31). It
maps to the **causal body** (``KaranaSarira``), which AV15 names as the *seed of
ignorance* persisting in deep sleep. Superimposing it therefore shades into
**mūlāvidyā** — the root ignorance — which README §17.2(3) marks as not fully
formalizable in classical logic (*avidyā* as *anādi*, beginningless). The check runs
the *same* superimposition test as for the other four sheaths, but **flags** the result
as bordering that limit, so an application (and AIM) treats it as the root case rather
than one error among five equals. It is never silently flattened, and never silently
dropped.
"""

from __future__ import annotations

from enum import Enum
from typing import final

from ..ontology import is_absolute, is_conditioned, is_subject
from ..report import Violation
from ..sorts import Obj, State


# ---------------------------------------------------------------------------
# The five sheaths (pañca-kośa) and their śarīra (body) associations
# ---------------------------------------------------------------------------

@final
class Sheath(Enum):
    """The five sheaths (*pañca-kośa*), with their body (*śarīra*) associations.

    Mapping (design doc §4/§9):
      * ANNAMAYA    — *deha* (gross body, ``SthulaSarira``)
      * PRANAMAYA   — vital sheath (subtle body, ``SukshmaSarira``)
      * MANOMAYA    — *manas* (subtle body, ``SukshmaSarira``)
      * VIJNANAMAYA — *vijñāna* (subtle body, ``SukshmaSarira``)
      * ANANDAMAYA  — *ānanda* (causal body, ``KaranaSarira``) — the seed of ignorance
    """

    ANNAMAYA = "annamaya"        # food/physical sheath — gross body
    PRANAMAYA = "prāṇamaya"      # vital sheath — subtle body
    MANOMAYA = "manomaya"        # mental sheath — subtle body
    VIJNANAMAYA = "vijñānamaya"  # intellect sheath — subtle body
    ANANDAMAYA = "ānandamaya"    # bliss sheath — causal body (seed of ignorance)

    @property
    def body(self) -> str:
        return {
            Sheath.ANNAMAYA: "sthūla-śarīra (gross body)",
            Sheath.PRANAMAYA: "sūkṣma-śarīra (subtle body)",
            Sheath.MANOMAYA: "sūkṣma-śarīra (subtle body)",
            Sheath.VIJNANAMAYA: "sūkṣma-śarīra (subtle body)",
            Sheath.ANANDAMAYA: "kāraṇa-śarīra (causal body, seed of ignorance)",
        }[self]

    @property
    def is_root(self) -> bool:
        """Is this the *ānandamaya* (causal-body) sheath — the root/subtlest case?"""
        return self is Sheath.ANANDAMAYA


#: The formalization limit the ānandamaya superimposition borders (README §17.2(3)).
ANANDAMAYA_LIMIT = "§17.2(3) — anādi-avidyā (mūlāvidyā: the beginninglessness of ignorance)"


def check_sheath_superimposition(sheath: Sheath, substrate: Obj) -> Violation | None:
    """Diagnose ``Superimposed(<sheath>, Y)`` — identifying the user with a sheath.

    This is the central diagnostic of the AIM bridge (Tier 2, design doc §9): an
    *adhyāsa* (M6/M7) in which a conditioned sheath is superimposed upon the witness.
    A non-``None`` return means the misidentification is present (the substrate is the
    Absolute, so the superimposition genuinely lands on Y as its locus — though by M8
    Y itself is untouched).

    If the substrate is *not* the Absolute, there is no sheath-on-Self superimposition
    to diagnose, and we return ``None`` (M7: superimposition's substrate is always the
    Absolute).

    The *ānandamaya* case (ruling (b)) runs the same test but flags the result as
    bordering the *mūlāvidyā* limit via :attr:`Violation.borders_limit`.
    """
    if not is_absolute(substrate):
        # M7: a superimposition's substrate is the Absolute. If the claimed substrate
        # is conditioned, this is not a sheath-on-Self misidentification.
        return None

    base_explanation = (
        f"Superimposed({sheath.value}, Y): the {sheath.value} sheath "
        f"({sheath.body}) is identified with the witness Y. By M6 the sheath is "
        f"conditioned; by M7 its substrate is the Absolute; this is adhyāsa — "
        f"misidentifying the Self with a conditioned sheath. By M8 the witness itself "
        f"remains untouched (asaṅga); the error is the jīva's cognition, not a change in Y."
    )
    reframe = (
        f"Treat the {sheath.value} sheath as a conditioned layer that *appears in* the "
        f"witness, not as the witness. 'I am not the {sheath.body}.'"
    )

    if sheath.is_root:
        # Ruling (b): same check, but marked as the root/mūlāvidyā-bordering case.
        return Violation(
            axiom_id="M6/M7 + AV15",
            term="ānandamaya-adhyāsa (mūlāvidyā)",
            explanation=(
                base_explanation
                + " This is the *subtlest* superimposition: the ānandamaya sheath is the "
                "causal body (KaranaSarira), which AV15 identifies as the seed of "
                "ignorance persisting in deep sleep (suṣupti). It is the root case — "
                "not one sheath-error among equals."
            ),
            reframe=reframe,
            borders_limit=ANANDAMAYA_LIMIT,
        )

    return Violation(
        axiom_id="M6/M7",
        term=f"{sheath.value}-adhyāsa",
        explanation=base_explanation,
        reframe=reframe,
    )


# ---------------------------------------------------------------------------
# AV-series state axioms
# ---------------------------------------------------------------------------

def check_av1_unique_state(jiva: Obj, state_count: int) -> Violation | None:
    """AV1 (AV1a/AV1b) — every jīva is in exactly one state at a time."""
    if state_count != 1:
        return Violation(
            axiom_id="AV1",
            term="avasthā",
            explanation=(
                f"AV1: a jīva is in exactly one state (waking/dream/deep-sleep) at a "
                f"time. {jiva!r} is reported as being in {state_count} states."
            ),
        )
    return None


def check_av11_deep_sleep_no_manifestation(state: State, manifests_something: bool) -> Violation | None:
    """AV11 — in deep sleep (*suṣupti*), nothing whatsoever manifests.

    The linchpin of the three-state argument: total withdrawal of manifestation.
    """
    if state is State.SUSUPTI and manifests_something:
        return Violation(
            axiom_id="AV11",
            term="suṣupti (deep sleep)",
            explanation=(
                "AV11: in deep sleep, nothing manifests to the jīva — total withdrawal "
                "of the manifest world. Something is reported as manifesting in suṣupti, "
                "which contradicts AV11."
            ),
        )
    return None


def check_av15_causal_body_persists(state: State, causal_body_persists: bool) -> Violation | None:
    """AV15 — in deep sleep, the causal body (seed of ignorance) persists.

    Even when nothing manifests (AV11), the causal body (``KaranaSarira``) remains as
    the *upādhi* of the jīva — the seed of *avidyā* from which waking/dream re-emerge.
    This is why the *ānandamaya* superimposition (above) borders *mūlāvidyā*.
    """
    if state is State.SUSUPTI and not causal_body_persists:
        return Violation(
            axiom_id="AV15",
            term="kāraṇa-śarīra (causal body)",
            explanation=(
                "AV15: in deep sleep the causal body (the seed of ignorance) persists as "
                "the jīva's limiting adjunct. It is reported as absent — but if it did "
                "not persist, there would be nothing from which waking re-emerges, and "
                "no continuity of the ignorant jīva."
            ),
        )
    return None


def check_av16_witness_persists(witness_present_in_all_states: bool) -> Violation | None:
    """AV16 — the witness (Y) persists through all three states."""
    if not witness_present_in_all_states:
        return Violation(
            axiom_id="AV16",
            term="sākṣin / turīya",
            explanation=(
                "AV16: the witness persists through all states (waking, dream, deep "
                "sleep) — it is the constant on which the changing states appear. "
                "The witness is reported as absent in some state."
            ),
        )
    return None


def check_av18_witness_no_state(entity: Obj, in_some_state: bool) -> Violation | None:
    """AV18 — the witness is never *in* any state (it is *turīya*, the fourth).

    Structurally enforced for ``SELF`` (``SELF.in_state`` always returns ``False``);
    this check catches a *claim* that places Y in a state.
    """
    if is_subject(entity) and in_some_state:
        return Violation(
            axiom_id="AV18",
            term="turīya",
            explanation=(
                f"AV18: the witness Y is never in any state — it is turīya, the fourth, "
                f"transcending waking/dream/deep-sleep. {entity!r} is the witness but is "
                f"claimed to be *in* a state. The witness persists through states (AV16) "
                f"without being one."
            ),
            reframe=(
                "States are conditions of the jīva (the conditioned subject). Attribute "
                "the state to the jīva, not to Y."
            ),
        )
    return None


def check_av22_criterion(entity: Obj, manifests_in_one_state: bool,
                          absent_in_another_state: bool) -> Violation | None:
    """AV22 — the criterion of reality: transience implies non-Absolute.

    If ``entity`` is claimed to be the Absolute yet manifests in one state and is
    absent in another (transient), AV22 is violated — what comes and goes is not
    ultimately real. (See also :func:`scherf.levels.appears_transient_so_not_absolute`,
    which classifies an output rather than checking an entity's claimed status.)
    """
    transient = manifests_in_one_state and absent_in_another_state
    if transient and is_absolute(entity):
        return Violation(
            axiom_id="AV22/AV23",
            term="sat (the real) vs. transient appearance",
            explanation=(
                f"AV22: what appears in one state but not another cannot be the Absolute. "
                f"{entity!r} is claimed to be the Absolute yet is transient across states. "
                f"(AV23: the Absolute never manifests empirically in the first place.)"
            ),
        )
    return None


def check_av23_absolute_no_manifestation(entity: Obj, manifests: bool) -> Violation | None:
    """AV23 — the Absolute never manifests empirically (in any state, to any jīva)."""
    if is_absolute(entity) and manifests:
        return Violation(
            axiom_id="AV23",
            term="aparokṣa (never an empirical object)",
            explanation=(
                f"AV23: the Absolute never manifests empirically to a jīva in any state. "
                f"{entity!r} is the Absolute but is reported as manifesting — the "
                f"Absolute is the witness in which manifestation occurs, never a "
                f"manifested object."
            ),
        )
    return None


def check_av24_av25_conditioned(entity: Obj, kind: str) -> Violation | None:
    """AV24a/b/c & AV25 — bodies (gross/subtle/causal) and the world are Conditioned."""
    if not is_conditioned(entity):
        return Violation(
            axiom_id="AV24/AV25",
            term="śarīra / jagat",
            explanation=(
                f"AV24/AV25: bodies (gross, subtle, causal) and world-entities are "
                f"Conditioned. {entity!r} (a {kind}) is not Conditioned — but only the "
                f"Absolute is unconditioned, and no body or world is the Absolute "
                f"(the 'You are not the body/mind/world' corollaries)."
            ),
        )
    return None
