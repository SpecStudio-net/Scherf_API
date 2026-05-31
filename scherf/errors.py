"""Exceptions for the Scherf library.

A small, dependency-free base used across the package. We distinguish two things
deliberately (see the design doc, docs/task1-design.md §1 and §10):

  * **Ontology-integrity errors** (this module) are raised when code tries to build
    a structurally impossible entity — e.g. a second Absolute (A2), or the witness
    `Y` carrying a profile (A13/AV18). These are *programming* errors: the library
    refuses to construct an ontology that contradicts the axioms.

  * **Claim violations** (added later, with the engine) are *not* exceptions. When an
    application asserts a claim and asks `check()` whether it is consistent with
    witness-centered principles, the answer is a *report* that names the offending
    axiom and explains why — never a raised error. A "violation" is always a property
    of the claim, never of `Y`.
"""

from __future__ import annotations


class AdvaitaError(Exception):
    """Base class for all Scherf-library errors.

    Raised only for ontology-integrity violations (see module docstring) — never for
    the routine checking of application claims.
    """
