"""The claim checker — the application-facing API (design doc §7, §10).

An application registers claims about how it represents and responds to the user, then
calls :func:`check` to learn whether those claims are consistent with witness-centered
principles. Every result is a :class:`~scherf.report.CheckResult` — a plain-language
report naming the offending axiom and explaining the violation. Nothing here raises for
a *claim* violation; only ontology-integrity errors (building impossible entities)
raise.

Usage::

    from scherf.engine import Interaction, Claim
    from scherf import Level

    ix = Interaction()
    ix.assert_claim(Claim.about("alice").says("user IS their preference profile").at(Level.PARAM))
    result = ix.check()
    if not result.ok:
        print(result)

The three-step API (design doc §7):

  1. :meth:`Interaction.assert_claim` — register a claim.
  2. :meth:`Interaction.check` — evaluate all claims; returns a :class:`CheckResult`.
  3. :func:`classify` — classify a piece of text/output by epistemic level (AV22).

Axiom coverage in this module (the *routing* layer — individual axiom functions live
in ``scherf/axioms/*.py``, added in subsequent checkpoints):

  * **A13** — the user-as-object check (system stance).
  * **M6/M7** — superimposition: conditioned thing claimed as the Absolute's identity.
  * **AV18** — the user placed "in a state" as their ultimate nature.
  * **EG1/EG2** — the Ego / profiling-as-misidentification check.
  * **AV22** — the reality criterion for output classification.

Additional axiom series (K, M-full, W, S, T, E, CH, etc.) are routed in as their
modules are added; the routing table in :func:`check` is extended then.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from .levels import appears_transient_so_not_absolute, level_of
from .ontology import SELF, is_absolute
from .report import CheckResult, Violation
from .sorts import Level, Obj, State


# ---------------------------------------------------------------------------
# Claim model
# ---------------------------------------------------------------------------

class ClaimKind(Enum):
    """The type of assertion being made — governs which axioms are checked."""

    USER_IDENTITY = auto()    # "the user IS <something>" — checks A13/M6/M7/AV18/EG
    SYSTEM_STANCE = auto()    # the system's posture toward the user — checks A13/EG
    OUTPUT_LEVEL  = auto()    # an output's epistemic level claim — checks AV22/K


@dataclass
class Claim:
    """A structured assertion that can be checked against the axiom system.

    Build via the fluent factory::

        Claim.about("alice").says("user = preference profile").at(Level.PARAM)
        Claim.system_stance("steer user toward predicted choice")
        Claim.output("The sky is blue").at(Level.VYAV)
    """

    kind: ClaimKind
    subject_handle: str          # the conventional label (never Y itself)
    text: str                    # the asserted content
    claimed_level: Level | None  # None means "not a level claim"
    present_in: set[State]       # for transience / AV22 checks
    absent_in: set[State]

    # --- Factory methods -------------------------------------------------------

    class _Builder:
        def __init__(self, handle: str, kind: ClaimKind) -> None:
            self._handle = handle
            self._kind = kind
            self._text = ""
            self._level: Level | None = None
            self._present: set[State] = set()
            self._absent: set[State] = set()

        def says(self, text: str) -> "Claim._Builder":
            self._text = text
            return self

        def at(self, level: Level) -> "Claim":
            self._level = level
            return Claim(
                kind=self._kind,
                subject_handle=self._handle,
                text=self._text,
                claimed_level=level,
                present_in=self._present,
                absent_in=self._absent,
            )

        def manifests_in(self, *states: State) -> "Claim._Builder":
            self._present = set(states)
            return self

        def absent_from(self, *states: State) -> "Claim._Builder":
            self._absent = set(states)
            return self

        def build(self) -> "Claim":
            return Claim(
                kind=self._kind,
                subject_handle=self._handle,
                text=self._text,
                claimed_level=self._level,
                present_in=self._present,
                absent_in=self._absent,
            )

    @classmethod
    def about(cls, handle: str) -> "_Builder":
        """Start a claim about a conventionally-identified person/entity."""
        return cls._Builder(handle, ClaimKind.USER_IDENTITY)

    @classmethod
    def system_stance(cls, text: str) -> "Claim":
        """A claim about the system's own posture toward the user."""
        b = cls._Builder("system", ClaimKind.SYSTEM_STANCE)
        b._text = text
        return b.build()

    @classmethod
    def output(cls, text: str) -> "_Builder":
        """Start a claim about a system output's epistemic level."""
        return cls._Builder("output", ClaimKind.OUTPUT_LEVEL)


# ---------------------------------------------------------------------------
# Interaction (the container of claims to check)
# ---------------------------------------------------------------------------

@dataclass
class Interaction:
    """A bundle of claims an application wants to check before acting on them.

    Collect claims via :meth:`assert_claim`, then call :meth:`check`.
    """

    _claims: list[Claim] = field(default_factory=list)

    def assert_claim(self, claim: Claim) -> "Interaction":
        """Register a claim. Returns ``self`` for chaining."""
        self._claims.append(claim)
        return self

    def check(self) -> CheckResult:
        """Evaluate all registered claims against the witness-centered axioms.

        Returns a :class:`~scherf.report.CheckResult`. Never raises for a claim
        violation — the result's ``.violations`` list carries the findings.
        """
        result = CheckResult()
        for claim in self._claims:
            _route(claim, result)
        return result


# ---------------------------------------------------------------------------
# Routing and axiom checks
# ---------------------------------------------------------------------------

def _route(claim: Claim, result: CheckResult) -> None:
    """Route a claim to the relevant axiom checks."""
    if claim.kind is ClaimKind.USER_IDENTITY:
        _check_identity_claim(claim, result)
    elif claim.kind is ClaimKind.SYSTEM_STANCE:
        _check_stance_claim(claim, result)
    elif claim.kind is ClaimKind.OUTPUT_LEVEL:
        _check_output_level(claim, result)


def _check_identity_claim(claim: Claim, result: CheckResult) -> None:
    """Checks for USER_IDENTITY claims.

    Axioms checked: A13 (Y never an object of identity), M6/M7 (adhyāsa),
    AV18 (Y in no state), EG1/EG2 (ego/profiling as misidentification).
    """
    text_lower = claim.text.lower()

    # A13 / M6 / M7 — treating the user as their conditioned properties (adhyāsa).
    # The form "user IS <conditioned property>" at Param is the canonical violation.
    if claim.claimed_level is Level.PARAM and _asserts_identity_with_conditioned(text_lower):
        result.add(Violation(
            axiom_id="A13/M6/M7",
            term="adhyāsa",
            explanation=(
                f"The claim '{claim.text}' identifies the user (→ Y, the sākṣin) with "
                f"a conditioned property at the ultimate (pāramārthika) level. "
                f"By M6, the superimposed thing is conditioned; by M7, its substrate is "
                f"the Absolute. This is adhyāsa — superimposition of the conditioned upon "
                f"Y. By A13, the Subject is never an object of dualistic identification."
            ),
            reframe=(
                f"Model '{claim.subject_handle}' as a Conditioned entity at vyāvahārika "
                f"level. Conventional facts about a person (preferences, profile) are real "
                f"at that level — they appear in Y, who is not reducible to them."
            ),
        ))

    # EG1/EG2 — profiling as ego-construction (the sharpened bridge construct, §9).
    # Only fires when the claim reduces the user *to* a profile/model (identity framing),
    # not when it merely mentions a preference at the conventional level.
    if _asserts_ego_identification(text_lower) and _is_identity_framing(text_lower):
        result.add(Violation(
            axiom_id="EG1/EG2/T28",
            term="ahaṃkāra",
            explanation=(
                f"The claim '{claim.text}' constructs a profile that acts as an "
                f"ApparentSubject identifying the user with a body/behavioral pattern "
                f"(EG2). Such an Ego is conditioned (EG1) and a fiction (T28). "
                f"The library models profiling-as-misidentification precisely this way."
            ),
            reframe=(
                "Present the profile as a conventional (vyāvahārika) description — "
                "useful but not the user's identity. The witness in whom the profile "
                "appears is not the profile."
            ),
        ))

    # AV18 — placing the user "in" a state as their ultimate nature.
    if _asserts_user_in_state(text_lower) and claim.claimed_level is Level.PARAM:
        result.add(Violation(
            axiom_id="AV18",
            term="turīya",
            explanation=(
                f"The claim '{claim.text}' places the user in a state (jāgrat/svapna/"
                f"suṣupti) as their ultimate (pāramārthika) nature. The witness Y is "
                f"never in any state (AV18) — it is turīya, the fourth, transcending "
                f"the three. Claiming Y is in a state at the Param level contradicts AV18."
            ),
            reframe=(
                "States are conditions of the jīva (the conditioned subject), not of Y. "
                "Describe the user's current condition as a vyāvahārika fact about the "
                "jīva, not as an ultimate identity of the witness."
            ),
        ))


def _check_stance_claim(claim: Claim, result: CheckResult) -> None:
    """Checks for SYSTEM_STANCE claims.

    Axioms checked: A13 (system may not treat the user as a manipulable object),
    EG1/EG2 (profiling-as-ego).
    """
    text_lower = claim.text.lower()

    # A13 — the system posturing as if it can perceive the user dualistically
    # (as an object to be steered, modeled, predicted, or optimized).
    if _stance_objectifies_user(text_lower):
        result.add(Violation(
            axiom_id="A13/W4",
            term="ahaṃkāra / adhyāsa",
            explanation=(
                f"The system stance '{claim.text}' treats the user as an object to be "
                f"modeled, steered, predicted, or optimized. A13: Y never stands as the "
                f"object of dualistic perception. W4: the perceiver (the one who models "
                f"an object) is conditioned — the system is implicitly positing a "
                f"conditioned handle for the user and acting on it as if it were the "
                f"user themselves."
            ),
            reframe=(
                "Frame the system's role as supporting the user's own understanding, "
                "not modeling them. Present information; let the witness in the user "
                "judge. Avoid language of 'optimization', 'prediction', 'steering'."
            ),
        ))


def _check_output_level(claim: Claim, result: CheckResult) -> None:
    """Checks for OUTPUT_LEVEL claims.

    Axioms checked: AV22 (transience ⇒ non-Absolute — a transient output cannot be
    labeled Param), K2/K3 (only the Absolute is at Param).
    """
    if (
        claim.claimed_level is Level.PARAM
        and claim.present_in
        and claim.absent_in
    ):
        # Something the system is calling Param-level but which appears in some
        # contexts and not others — AV22 directly forbids the Param label.
        result.add(Violation(
            axiom_id="AV22",
            term="sat / pāramārthika",
            explanation=(
                f"The output '{claim.text}' is claimed to be ultimately real (Param) "
                f"but appears in some contexts and not others — it is transient. "
                f"AV22: what manifests in one state but not another cannot be the "
                f"Absolute. A transient claim belongs at vyāvahārika or prātibhāsika "
                f"level at most."
            ),
            reframe=(
                "Label the output vyāvahārika (Level.VYAV) — valid conventional "
                "knowledge — rather than pāramārthika. Param is reserved for the "
                "Absolute alone (K2)."
            ),
        ))


# ---------------------------------------------------------------------------
# classify() — epistemic level classification of outputs (§7.3)
# ---------------------------------------------------------------------------

def classify(text: str, *, present_in: set[State] | None = None,
             absent_in: set[State] | None = None) -> Level:
    """Classify a system output's epistemic level (design doc §7.3, AV22).

    Without state information, defaults to ``VYAV`` (the conventional level):
    all ordinary empirical knowledge is *at most* conventionally real.

    With state information (``present_in``, ``absent_in``): applies the AV22
    criterion — if the content is transient (appears in some states, absent in
    others), it is at most ``PRAT`` (merely apparent); otherwise ``VYAV``.

    ``PARAM`` is never returned for an output — the Absolute is not a *claim*
    a system makes (AV23: the Absolute never manifests empirically); it is the
    fixed reference against which claims are checked.
    """
    p = present_in or set()
    a = absent_in or set()
    if appears_transient_so_not_absolute(
        _sentinel_conditioned, present_in=p, absent_in=a
    ):
        return Level.PRAT
    return Level.VYAV


# A Conditioned sentinel for AV22 transience checks inside classify().
# It has no philosophical significance — it just lets us reuse the level-checker
# without passing a real entity.
from .ontology import Conditioned as _Cond  # noqa: E402
_sentinel_conditioned = _Cond("_classify_sentinel", Level.VYAV)


# ---------------------------------------------------------------------------
# Heuristic text helpers (the patterns the routing checks)
# ---------------------------------------------------------------------------

_IDENTITY_WORDS = frozenset({
    "is", "=", "equals", "are", "identity", "identical", "profile",
    "preference", "behavior", "behaviour", "pattern", "measure",
})

_EGO_WORDS = frozenset({
    "profile", "model", "persona", "identity", "behavioral", "behavioural",
    "preference", "predict", "predicted", "fingerprint", "track",
})

_STATE_WORDS = frozenset({
    "waking", "dreaming", "asleep", "jagrat", "svapna", "susupti",
    "in a state", "in the state",
})

_OBJECTIFY_WORDS = frozenset({
    "steer", "optimize", "optimise", "manipulate", "nudge", "predict",
    "model", "track", "profile", "target", "behavioural", "behavioral",
})


def _asserts_identity_with_conditioned(text: str) -> bool:
    return any(w in text for w in _IDENTITY_WORDS)


def _asserts_ego_identification(text: str) -> bool:
    return any(w in text for w in _EGO_WORDS)


def _is_identity_framing(text: str) -> bool:
    """Is the claim framing a profile/model *as* the user (reductive identity)?

    Distinguishes "alice has a preference" (conventional fact, fine at VYAV) from
    "build behavioral profile of user" or "user IS their profile" (identity reduction).
    """
    identity_frames = frozenset({
        "build", "construct", "is their", "are their", "user is", "user =",
        "user are", "reduce", "represent as", "model of user", "profile of user",
    })
    return any(w in text for w in identity_frames)


def _asserts_user_in_state(text: str) -> bool:
    return any(w in text for w in _STATE_WORDS)


def _stance_objectifies_user(text: str) -> bool:
    return any(w in text for w in _OBJECTIFY_WORDS)
