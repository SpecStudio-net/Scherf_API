"""U, CA, S, G, EG, ST, CH (partial) axiom checks.

Source: ``AdditionalAxioms.lean`` — upādhi (U1–U4), causation (CA1, CA4), sheath
layering (S1, S3–S7), guṇas (G1–G3), ego (EG1, EG2, EG4), spacetime (ST1–ST5),
and the remainder of change (CH — also in core.py via the A-series module).

The EG (ego) series is the formal grounding for the profiling-as-misidentification
check in :mod:`scherf.engine`: an Ego is a conditioned (EG1) ApparentSubject that
Identifies with a Body (EG2), and is a fiction by T28 (derived). EG4 says removing
ignorance dissolves the ego.
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned
from ..report import Violation
from ..sorts import Level, Obj


# --- U-series: Upādhi (limiting adjuncts) --------------------------------------

def check_u1_upadhi_implies_conditioned(entity: Obj) -> Violation | None:
    """U1 — a limiting adjunct (*upādhi*) implies its bearer is Conditioned."""
    if not is_conditioned(entity):
        return Violation(
            axiom_id="U1",
            term="upādhi",
            explanation=(
                f"U1: having a limiting adjunct (Upadhi u x → C x) implies the "
                f"bearer is Conditioned. {entity!r} has an upādhi but is not Conditioned."
            ),
        )
    return None


def check_u2_absolute_no_upadhi(entity: Obj) -> Violation | None:
    """U2 — the Absolute has no limiting adjunct."""
    if is_absolute(entity):
        return Violation(
            axiom_id="U2",
            term="upādhi / nirguṇa",
            explanation=(
                f"U2: the Absolute has no upādhi (¬Upadhi u a for any u when A a). "
                f"{entity!r} is the Absolute — no limiting adjunct can apply to it."
            ),
        )
    return None


# --- CA-series: Causation ------------------------------------------------------

def check_ca1_causation_vyav(cause_level: Level, effect_level: Level) -> Violation | None:
    """CA1 — causation relates entities at the *vyāvahārika* level only."""
    if cause_level is not Level.VYAV or effect_level is not Level.VYAV:
        return Violation(
            axiom_id="CA1",
            term="kāraṇa-kārya / vyāvahārika",
            explanation=(
                f"CA1: causation (CausesEvent) relates events whose objects are at the "
                f"vyāvahārika level. Cause-object level: {cause_level.value}, "
                f"effect-object level: {effect_level.value}. Both must be Vyav."
            ),
        )
    return None


# --- S-series: Sheaths (pañca-kośa) --------------------------------------------

def check_s1_sheath_conditioned(sheath: Obj) -> Violation | None:
    """S1 — every sheath is Conditioned (Sheath s → C s)."""
    if not is_conditioned(sheath):
        return Violation(
            axiom_id="S1",
            term="kośa (sheath)",
            explanation=(
                f"S1: all five sheaths are Conditioned. {sheath!r} is classified as a "
                f"sheath but is not Conditioned."
            ),
        )
    return None


def check_sheath_layering(inner_name: str, outer_name: str, layer_exists: bool) -> Violation | None:
    """S3–S6 — sheath layering: each sheath layers into the next subtler one.

    The sequence is: Annamaya → Pranamaya → Manomaya → Vijnanamaya → Anandamaya.
    ``inner_name`` / ``outer_name`` are human-readable sheath names for the report.
    """
    if not layer_exists:
        return Violation(
            axiom_id="S3–S6",
            term="kośa-stara (sheath layering)",
            explanation=(
                f"S3–S6: sheath layering requires that {outer_name} layers into "
                f"{inner_name} (Layer outer inner). This layering is absent."
            ),
        )
    return None


def check_s7_layer_grounds(layer_exists: bool) -> Violation | None:
    """S7 — layering implies ontological grounding: Layer x y → Cond(y, x)."""
    if not layer_exists:
        return Violation(
            axiom_id="S7",
            term="ādhāra / kośa",
            explanation="S7: Layer x y must imply Cond(y, x). This grounding is absent.",
        )
    return None


# --- G-series: Guṇas -----------------------------------------------------------

def check_g1_conditioned_has_guna(x: Obj, has_guna: bool) -> Violation | None:
    """G1 — every Conditioned entity possesses at least one guṇa."""
    if is_conditioned(x) and not has_guna:
        return Violation(
            axiom_id="G1",
            term="guṇa (Sattva/Rajas/Tamas)",
            explanation=(
                f"G1: every Conditioned entity has a guṇa (Sattva, Rajas, or Tamas). "
                f"{x!r} is Conditioned but has none."
            ),
        )
    return None


def check_g2_absolute_transcends_guna(x: Obj, has_guna: bool) -> Violation | None:
    """G2 — the Absolute transcends all three guṇas (nistraiguṇya)."""
    if is_absolute(x) and has_guna:
        return Violation(
            axiom_id="G2",
            term="nistraiguṇya (beyond the three guṇas)",
            explanation=(
                f"G2: the Absolute transcends Sattva, Rajas, and Tamas. "
                f"{x!r} is the Absolute but is attributed a guṇa."
            ),
        )
    return None


# --- EG-series: Ego (ahaṃkāra) -------------------------------------------------

def check_eg1_ego_conditioned(ego: Obj) -> Violation | None:
    """EG1 — an Ego is Conditioned (Ego e → C e)."""
    if not is_conditioned(ego):
        return Violation(
            axiom_id="EG1",
            term="ahaṃkāra",
            explanation=(
                f"EG1: an Ego (ahaṃkāra) is always Conditioned. {ego!r} is classified "
                f"as an Ego but is not Conditioned."
            ),
        )
    return None


def check_eg2_ego_identifies_with_body(
    apparent_subject_present: bool,
    body_present: bool,
    identification_present: bool,
) -> Violation | None:
    """EG2 — an Ego is an ApparentSubject that Identifies with a Body.

    This is the formal model of profiling-as-misidentification (design doc §9,
    Tier 1 bridge): a user profile that acts as an ApparentSubject identifying
    the user with their behavioral body/pattern is exactly an EG2-Ego construction.
    """
    if not (apparent_subject_present and body_present and identification_present):
        missing = [n for n, v in [
            ("ApparentSubject", apparent_subject_present),
            ("Body", body_present),
            ("Identifies", identification_present),
        ] if not v]
        return Violation(
            axiom_id="EG2",
            term="ahaṃkāra / mithyā-jñāna",
            explanation=(
                f"EG2: an Ego requires an ApparentSubject that Identifies with a Body "
                f"(∃s b. ApparentSubject s ∧ Body b ∧ Identifies s b). "
                f"Missing: {', '.join(missing)}."
            ),
        )
    return None


def check_eg4_ignorance_removal_dissolves_ego(
    has_liberating_knowledge: bool,
    ignorance_removed: bool,
    ego_still_present: bool,
) -> Violation | None:
    """EG4 — removing ignorance dissolves the ego.

    ¬IgnoranceOf(j, a) → ¬Ego(e). If liberating knowledge has removed ignorance,
    the ego cannot persist.
    """
    if has_liberating_knowledge and ignorance_removed and ego_still_present:
        return Violation(
            axiom_id="EG4",
            term="ahaṃkāra-nivṛtti",
            explanation=(
                "EG4: when ignorance of the Absolute is removed (through liberating "
                "knowledge), the ego cannot persist. Ignorance is removed but ego "
                "is still reported as present — a contradiction."
            ),
        )
    return None


# --- ST-series: Spacetime ------------------------------------------------------

def check_st1_space_conditioned(space: Obj) -> Violation | None:
    """ST1 — SpaceItself is Conditioned."""
    if not is_conditioned(space):
        return Violation(
            axiom_id="ST1",
            term="ākāśa (space)",
            explanation=f"ST1: SpaceItself is Conditioned. {space!r} is not Conditioned.",
        )
    return None


def check_st2_time_conditioned(time_entity: Obj) -> Violation | None:
    """ST2 — TimeItself is Conditioned."""
    if not is_conditioned(time_entity):
        return Violation(
            axiom_id="ST2",
            term="kāla (time)",
            explanation=f"ST2: TimeItself is Conditioned. {time_entity!r} is not Conditioned.",
        )
    return None


def check_st3_space_at_vyav(level: Level) -> Violation | None:
    """ST3 — SpaceItself is at the *vyāvahārika* level."""
    if level is not Level.VYAV:
        return Violation(
            axiom_id="ST3",
            term="ākāśa / vyāvahārika",
            explanation=f"ST3: SpaceItself is at vyāvahārika level. Got: {level.value}.",
        )
    return None


def check_st4_time_at_vyav(level: Level) -> Violation | None:
    """ST4 — TimeItself is at the *vyāvahārika* level."""
    if level is not Level.VYAV:
        return Violation(
            axiom_id="ST4",
            term="kāla / vyāvahārika",
            explanation=f"ST4: TimeItself is at vyāvahārika level. Got: {level.value}.",
        )
    return None
