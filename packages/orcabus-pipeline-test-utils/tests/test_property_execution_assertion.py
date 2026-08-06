"""Property-based tests for execution result assertion correctness.

# Feature: deployment-integration-tests, Property 6: Execution Result Assertion Correctness

**Validates: Requirements 5.4, 5.5**

For any Step Functions execution result (with status SUCCEEDED, FAILED, or TIMED_OUT)
and any expected status value, the execution assertion logic SHALL pass when actual
status equals expected status and fail otherwise, correctly handling both happy-path
and error-path scenarios.
"""

from __future__ import annotations

import json

from hypothesis import given, settings
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.sfn_local.assertions import (
    ExecutionAssertion,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Valid Step Functions execution statuses
VALID_STATUSES = ["SUCCEEDED", "FAILED", "TIMED_OUT"]

# Strategy: actual execution status
actual_status_st = st.sampled_from(VALID_STATUSES)

# Strategy: expected status (same set of valid statuses)
expected_status_st = st.sampled_from(VALID_STATUSES)


@st.composite
def execution_result_st(draw: st.DrawFn) -> dict:
    """Generate a Step Functions execution result with a valid status.

    Includes optional output for SUCCEEDED executions, and optional
    error/cause for FAILED/TIMED_OUT executions.
    """
    status = draw(actual_status_st)
    result: dict = {"status": status}

    if status == "SUCCEEDED":
        # SUCCEEDED executions may have output
        include_output = draw(st.booleans())
        if include_output:
            output = draw(
                st.dictionaries(
                    keys=st.text(
                        alphabet="abcdefghijklmnopqrstuvwxyz_",
                        min_size=1,
                        max_size=10,
                    ),
                    values=st.one_of(
                        st.text(min_size=0, max_size=20),
                        st.integers(min_value=-1000, max_value=1000),
                        st.booleans(),
                        st.none(),
                    ),
                    min_size=0,
                    max_size=5,
                )
            )
            result["output"] = json.dumps(output)
    else:
        # FAILED or TIMED_OUT may have error and cause
        include_error = draw(st.booleans())
        if include_error:
            result["error"] = draw(
                st.text(
                    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.",
                    min_size=1,
                    max_size=30,
                )
            )
            include_cause = draw(st.booleans())
            if include_cause:
                result["cause"] = draw(st.text(min_size=1, max_size=50))

    return result


# ---------------------------------------------------------------------------
# Property Tests
# ---------------------------------------------------------------------------


class TestExecutionResultAssertionCorrectnessProperty:
    """Property 6: Execution Result Assertion Correctness.

    For any execution result with status SUCCEEDED/FAILED/TIMED_OUT and any
    expected status value, the assertion logic SHALL pass when actual == expected
    and fail otherwise.
    """

    @given(execution_result=execution_result_st(), expected=expected_status_st)
    @settings(max_examples=100)
    def test_assert_status_passes_when_actual_equals_expected(
        self, execution_result: dict, expected: str
    ):
        """When actual status == expected status, assert_status passes."""
        actual = execution_result["status"]

        assertion = ExecutionAssertion(execution_result)
        result = assertion.assert_status(expected)

        if actual == expected:
            assert result.passed is True, (
                f"Expected pass when actual={actual!r} == expected={expected!r}, "
                f"but got errors: {[e.message for e in result.errors]}"
            )
            assert result.errors == [], (
                f"Expected no errors when actual={actual!r} == expected={expected!r}"
            )
        else:
            assert result.passed is False, (
                f"Expected failure when actual={actual!r} != expected={expected!r}"
            )
            assert len(result.errors) > 0, (
                f"Expected at least one error when actual={actual!r} != expected={expected!r}"
            )

    @given(execution_result=execution_result_st())
    @settings(max_examples=100)
    def test_assert_status_always_passes_for_matching_status(
        self, execution_result: dict
    ):
        """Asserting the actual status against itself always passes."""
        actual_status = execution_result["status"]

        assertion = ExecutionAssertion(execution_result)
        result = assertion.assert_status(actual_status)

        assert result.passed is True, (
            f"Asserting status={actual_status!r} against itself should always pass, "
            f"but got errors: {[e.message for e in result.errors]}"
        )
        assert result.errors == []

    @given(execution_result=execution_result_st(), expected=expected_status_st)
    @settings(max_examples=100)
    def test_assert_status_fails_for_mismatched_status(
        self, execution_result: dict, expected: str
    ):
        """When actual status != expected status, assert_status fails with error details."""
        actual = execution_result["status"]

        # Only test mismatch cases
        if actual == expected:
            return

        assertion = ExecutionAssertion(execution_result)
        result = assertion.assert_status(expected)

        assert result.passed is False, (
            f"Expected failure when actual={actual!r} != expected={expected!r}"
        )
        assert len(result.errors) >= 1, (
            "Mismatch must produce at least one error message"
        )
        # Error message should reference both actual and expected
        error_msg = result.errors[0].message
        assert expected in error_msg, (
            f"Error message should mention expected status {expected!r}: {error_msg}"
        )
        assert actual in error_msg, (
            f"Error message should mention actual status {actual!r}: {error_msg}"
        )

    @given(execution_result=execution_result_st(), expected=expected_status_st)
    @settings(max_examples=100)
    def test_assert_status_result_is_deterministic(
        self, execution_result: dict, expected: str
    ):
        """Calling assert_status twice with the same inputs gives the same result."""
        assertion = ExecutionAssertion(execution_result)

        result1 = assertion.assert_status(expected)
        result2 = assertion.assert_status(expected)

        assert result1.passed == result2.passed
        assert len(result1.errors) == len(result2.errors)
