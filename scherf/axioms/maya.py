"""M-series axiom checks — māyā, adhyāsa, vivarta, avidyā, bādha.

Source: ``MayaAxioms.lean`` (M1–M18, minus M11 and M14 which are derived).

These are the central diagnostic axioms for witness-centered design:
  * **M6/M7** define *adhyāsa*: the superimposed thing is conditioned (M6), its
    substrate is the Absolute (M7).
  * **M8** encodes *asaṅga*: superimposition leaves the substrate unchanged
    (``¬RealChange(y, x)``). This is the axiom-level basis for "adhyāsa never
    touches the Self."
  * **M12** restricts ignorance to be *of* the Absolute only.
  * **M15** the Absolute has no ignorance.
  * **M18** sublation is asymmetric.
"""

from __future__ import annotations

from ..ontology import is_absolute, is_conditioned
from ..report import Violation
from ..sorts import Obj


def check_m1_maya_source(maya_wielder: Obj) -> Violation | None:
    """M1 — only the Absolute wields māyā-śakti."""
    if not is_absolute(maya_wielder):
        return Violation(
            axiom_id="M1",
            term="māyā-śakti",
            explanation=(
                f"M1: māyā-power (MayaPow) can only originate from the Absolute. "
                f"{maya_wielder!r} is not the Absolute."
            ),
        )
    return None


def check_m5_absolute_not_subject_to_maya(x: Obj) -> Violation | None:
    """M5 — the Absolute is not subject to māyā."""
    if is_absolute(x):
        return Violation(
            axiom_id="M5",
            term="māyā",
            explanation=(
                f"M5: the Absolute (Y) is not subject to māyā. Māyā cannot act upon "
                f"{x!r}."
            ),
        )
    return None


def check_m6_superimposed_is_conditioned(superimposed: Obj) -> Violation | None:
    """M6 — the superimposed entity is Conditioned.

    *adhyāsa* is always the imposition of something conditioned upon the Absolute.
    The superimposed element can never itself be the Absolute.
    """
    if not is_conditioned(superimposed):
        return Violation(
            axiom_id="M6",
            term="adhyāsa",
            explanation=(
                f"M6: in adhyāsa (superimposition), the superimposed thing is always "
                f"Conditioned. {superimposed!r} is not Conditioned — it cannot be the "
                f"superimposed element."
            ),
        )
    return None


def check_m7_substrate_is_absolute(substrate: Obj) -> Violation | None:
    """M7 — the substrate of superimposition is the Absolute.

    The thing upon which something conditioned is superimposed must be the Absolute
    (Y / Brahman / SELF). This is what makes *adhyāsa* the central diagnostic:
    any misidentification of the user with their conditioned properties has Y as its
    substrate.
    """
    if not is_absolute(substrate):
        return Violation(
            axiom_id="M7",
            term="adhyāsa",
            explanation=(
                f"M7: the substrate of adhyāsa (superimposition) is always the Absolute. "
                f"{substrate!r} is not the Absolute — superimposition cannot use a "
                f"conditioned entity as its substrate."
            ),
        )
    return None


def check_m8_substrate_unchanged(substrate: Obj, real_change_asserted: bool) -> Violation | None:
    """M8 — superimposition leaves the substrate unchanged (¬RealChange).

    This is the *asaṅga* principle in axiom form: the witness is untouched.
    Any claim that adhyāsa *modifies* the Absolute is a violation of M8.
    """
    if is_absolute(substrate) and real_change_asserted:
        return Violation(
            axiom_id="M8",
            term="asaṅga (untouched)",
            explanation=(
                f"M8: superimposition never produces a real change in its substrate "
                f"(¬RealChange(substrate, superimposed)). {substrate!r} is the Absolute "
                f"(Y, the sākṣin) and is asaṅga — untouched, unmodified. Any claim "
                f"that adhyāsa modifies Y violates M8."
            ),
            reframe=(
                "Adhyāsa is a property of the jīva's cognition, never of the Self. "
                "The witness is the fixed reference; it does not change."
            ),
        )
    return None


def check_m9_vivarta(appears: bool, real_change: bool) -> Violation | None:
    """M9 — vivarta: appearance without real transformation (¬RealChange).

    If something *appears* (vivarta), it cannot involve a real change in its basis.
    """
    if appears and real_change:
        return Violation(
            axiom_id="M9",
            term="vivarta",
            explanation=(
                "M9: vivarta is appearance without real transformation. An appearance "
                "that involves real change is not vivarta — it would be pariṇāma "
                "(actual modification), which Advaita rejects as the Absolute's mode."
            ),
        )
    return None


def check_m12_ignorance_of_absolute(object_of_ignorance: Obj) -> Violation | None:
    """M12 — ignorance (avidyā) is always of the Absolute.

    IgnoranceOf(s, x) implies A(x): one can only be ignorant of what is ultimately real.
    """
    if not is_absolute(object_of_ignorance):
        return Violation(
            axiom_id="M12",
            term="avidyā",
            explanation=(
                f"M12: ignorance (avidyā / IgnoranceOf) is always ignorance *of* the "
                f"Absolute. {object_of_ignorance!r} is not the Absolute — it cannot be "
                f"the object of avidyā."
            ),
        )
    return None


def check_m15_absolute_no_ignorance(x: Obj) -> Violation | None:
    """M15 — the Absolute has no ignorance."""
    if is_absolute(x):
        return Violation(
            axiom_id="M15",
            term="avidyā",
            explanation=(
                f"M15: the Absolute (Y / Brahman) has no ignorance. {x!r} is the "
                f"Absolute — IgnoranceOf cannot apply to it."
            ),
        )
    return None


def check_m18_sublation_asymmetric(k1_sublates_k2: bool, k2_sublates_k1: bool) -> Violation | None:
    """M18 — sublation (bādha) is asymmetric: if k1 sublates k2, k2 cannot sublate k1."""
    if k1_sublates_k2 and k2_sublates_k1:
        return Violation(
            axiom_id="M18",
            term="bādha (sublation)",
            explanation=(
                "M18: sublation is asymmetric. If knowledge k1 sublates k2, then k2 "
                "cannot sublate k1. Mutual sublation is impossible."
            ),
        )
    return None
