"""Shared assertion utilities.

Provides reusable assertion primitives for all test harnesses:
- AssertionResult: Pass/fail dataclass with error accumulation
- match_json: Deep JSON comparison with wildcard support
- ANY_STRING_PLACEHOLDER: Wildcard marker for string-typed values
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


# Wildcard placeholder indicating "any string value"
ANY_STRING_PLACEHOLDER = "{% any_string %}"


@dataclass
class AssertionError_:
    """A single assertion failure with context."""

    message: str


@dataclass
class AssertionResult:
    """Result of running one or more assertions.

    Accumulates errors and tracks pass/fail state. Used by all assertion
    classes across the package.
    """

    passed: bool
    errors: list[AssertionError_] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error and mark the result as failed."""
        self.passed = False
        self.errors.append(AssertionError_(message=message))


def match_json(
    actual: object,
    expected: object,
    path: str = "$",
) -> list[str]:
    """Compare actual JSON against expected, respecting wildcard placeholders.

    The ``{% any_string %}`` placeholder in the expected structure indicates
    that the actual value must exist and be a string, but its exact value is
    not checked.

    Args:
        actual: The actual JSON value (parsed from execution output).
        expected: The expected JSON structure (may contain wildcards).
        path: JSONPath-style breadcrumb for error messages.

    Returns:
        A list of mismatch descriptions. Empty list means match.
    """
    errors: list[str] = []

    if expected == ANY_STRING_PLACEHOLDER:
        # Wildcard: actual must be a string
        if not isinstance(actual, str):
            errors.append(
                f"{path}: expected a string (wildcard), "
                f"got {type(actual).__name__}: {actual!r}"
            )
        return errors

    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            errors.append(
                f"{path}: expected an object, got {type(actual).__name__}"
            )
            return errors

        # Check all expected keys are present with correct values
        for key in expected:
            if key not in actual:
                errors.append(f"{path}.{key}: missing in actual output")
            else:
                errors.extend(
                    match_json(actual[key], expected[key], path=f"{path}.{key}")
                )

        # Check for unexpected keys in actual
        for key in actual:
            if key not in expected:
                errors.append(f"{path}.{key}: unexpected key in actual output")

        return errors

    if isinstance(expected, list):
        if not isinstance(actual, list):
            errors.append(
                f"{path}: expected an array, got {type(actual).__name__}"
            )
            return errors

        if len(actual) != len(expected):
            errors.append(
                f"{path}: array length mismatch: "
                f"actual={len(actual)}, expected={len(expected)}"
            )
            return errors

        for i, (a_item, e_item) in enumerate(zip(actual, expected)):
            errors.extend(match_json(a_item, e_item, path=f"{path}[{i}]"))

        return errors

    # Scalar comparison
    if actual != expected:
        errors.append(
            f"{path}: value mismatch: actual={actual!r}, expected={expected!r}"
        )

    return errors
