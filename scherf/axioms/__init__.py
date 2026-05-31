"""Axiom modules — one named function per Lean axiom.

Each function signature is: ``check_<id>(relevant args) -> Violation | None``.
``None`` means the axiom is satisfied; a ``Violation`` means it is not.

Axioms already enforced *structurally* by the type system (ontology.py / levels.py)
are documented here as identity functions that always return ``None`` — they cannot
be violated at runtime, but are named so the coverage is explicit.

Source of truth: ``docs/axiom-catalogue.md``.
"""
