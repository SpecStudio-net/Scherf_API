"""Violation reports — the human-legible output of the axiom checker.

A claim violation is never an exception (see :mod:`scherf.errors`). It is a
structured record naming the axiom, the IAST term, and a plain-language explanation
so that a developer (or you, the maintainer) can read the result without consulting
the Lean source.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class Violation:
    """A single axiom violation — a property of a *claim*, never of ``Y``.

    Attributes:
        axiom_id      Lean axiom identifier(s), e.g. ``"A13"`` or ``"M6/M7"``.
        term          IAST Sanskrit term, e.g. ``"adhyāsa"``.
        explanation   Plain-language reason the claim violates this axiom.
        reframe       Optional suggested witness-centered restatement.
        borders_limit Optional marker naming a formalization limit (README §17.2)
                      that this violation borders. When set, the violation is real but
                      shades into territory the formalism cannot fully capture — an
                      application should treat it as a *root* case, not as one ordinary
                      finding among equals. This is the explicit-marker mechanism of
                      design doc §11 (never silent approximation). The canonical use is
                      the *ānandamaya* (causal-body) superimposition, which borders
                      §17.2(3) — the beginninglessness of *avidyā* (*mūlāvidyā*).
    """

    axiom_id: str
    term: str
    explanation: str
    reframe: str = ""
    borders_limit: str = ""

    def __str__(self) -> str:
        lines = [f"[{self.axiom_id}] {self.term}: {self.explanation}"]
        if self.reframe:
            lines.append(f"  → Reframe: {self.reframe}")
        if self.borders_limit:
            lines.append(f"  ⚠ Borders formalization limit {self.borders_limit} — "
                         f"treat as a root case, not fully reducible to the others.")
        return "\n".join(lines)


@dataclass
class CheckResult:
    """The result of :func:`scherf.engine.check` on an :class:`~scherf.engine.Interaction`.

    Attributes:
        ok          ``True`` iff no violations were found.
        violations  The list of violations (empty when ``ok`` is ``True``).
    """

    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.violations) == 0

    def add(self, v: Violation) -> None:
        self.violations.append(v)

    def __str__(self) -> str:
        if self.ok:
            return "CheckResult: OK — no witness-centered violations found."
        lines = [f"CheckResult: {len(self.violations)} violation(s) found:"]
        for v in self.violations:
            lines.append("")
            lines.append(str(v))
        return "\n".join(lines)
