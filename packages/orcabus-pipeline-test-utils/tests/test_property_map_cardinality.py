"""Property-based tests for Map state output cardinality assertion.

# Feature: deployment-integration-tests, Property 10: Map State Output Cardinality

**Validates: Requirements 6.5**

For any Map state execution with an input array of length N, the Map state assertion
SHALL pass only when the output array has exactly N elements, and SHALL fail with a
descriptive error when the cardinality does not match.
"""

from __future__ import annotations

import json

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.sfn_local.assertions import (
    AssertionResult,
    ExecutionAssertion,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Strategy: arbitrary JSON-serializable values for array elements
json_primitive_st = st.one_of(
    st.integers(min_value=-1000, max_value=1000),
    st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
    st.text(min_size=0, max_size=50),
    st.booleans(),
    st.none(),
)

# Strategy: JSON-serializable values (including nested structures)
json_value_st = st.recursive(
    json_primitive_st,
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(
            st.text(min_size=1, max_size=10),
            children,
            max_size=5,
        ),
    ),
    max_leaves=10,
)

# Strategy: input arrays of varying length
input_array_st = st.lists(json_value_st, min_size=0, max_size=20)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_execution_result(
    status: str = "SUCCEEDED",
    output: list | dict | None = None,
) -> dict:
    """Create a mock execution result dict."""
    result: dict = {"status": status}
    if output is not None:
        result["output"] = json.dumps(output)
    return result


# ---------------------------------------------------------------------------
# Property Tests
# ---------------------------------------------------------------------------


class TestMapStateOutputCardinalityProperty:
    """Property 10: Map State Output Cardinality.

    For any Map state execution with an input array of length N, the Map state
    assertion SHALL pass only when the output array has exactly N elements, and
    SHALL fail with a descriptive error when the cardinality does not match.
    """

    @given(input_array=input_array_st)
    @settings(max_examples=100)
    def test_pass_when_output_length_equals_input_length(
        self, input_array: list
    ):
        """Assertion passes when output array has exactly N elements
        (same length as the input array)."""
        n = len(input_array)
        # Generate an output array with exactly N elements
        output_array = list(range(n))

        execution = _make_execution_result(output=output_array)
        assertion = ExecutionAssertion(execution)
        result = assertion.assert_map_state_output_cardinality(
            input_array=input_array
        )

        assert result.passed is True
        assert result.errors == []

    @given(input_array=input_array_st)
    @settings(max_examples=100)
    def test_pass_with_explicit_output_matching_length(
        self, input_array: list
    ):
        """Assertion passes when explicitly provided map_state_output has
        the same length as the input array."""
        n = len(input_array)
        map_state_output = [{"result": i} for i in range(n)]

        execution = _make_execution_result()
        assertion = ExecutionAssertion(execution)
        result = assertion.assert_map_state_output_cardinality(
            input_array=input_array,
            map_state_output=map_state_output,
        )

        assert result.passed is True
        assert result.errors == []

    @given(
        input_array=st.lists(json_value_st, min_size=1, max_size=20),
        extra=st.integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_fail_when_output_has_more_elements(
        self, input_array: list, extra: int
    ):
        """Assertion fails with descriptive error when output has more
        elements than the input array."""
        n = len(input_array)
        output_array = list(range(n + extra))

        execution = _make_execution_result(output=output_array)
        assertion = ExecutionAssertion(execution)
        result = assertion.assert_map_state_output_cardinality(
            input_array=input_array
        )

        assert result.passed is False
        assert len(result.errors) > 0
        error_msg = result.errors[0].message.lower()
        assert "cardinality" in error_msg or "mismatch" in error_msg

    @given(
        input_array=st.lists(json_value_st, min_size=2, max_size=20),
        fewer=st.integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_fail_when_output_has_fewer_elements(
        self, input_array: list, fewer: int
    ):
        """Assertion fails with descriptive error when output has fewer
        elements than the input array."""
        n = len(input_array)
        # Ensure we remove at least 1 but don't go below 0
        output_length = max(0, n - fewer)
        assume(output_length != n)  # Ensure lengths actually differ

        output_array = list(range(output_length))

        execution = _make_execution_result(output=output_array)
        assertion = ExecutionAssertion(execution)
        result = assertion.assert_map_state_output_cardinality(
            input_array=input_array
        )

        assert result.passed is False
        assert len(result.errors) > 0
        error_msg = result.errors[0].message.lower()
        assert "cardinality" in error_msg or "mismatch" in error_msg

    @given(input_array=input_array_st)
    @settings(max_examples=100)
    def test_fail_descriptive_error_includes_element_counts(
        self, input_array: list
    ):
        """When cardinality mismatches, the error message includes both
        the expected and actual element counts."""
        n = len(input_array)
        # Generate output with different length (n + 1)
        output_array = list(range(n + 1))

        execution = _make_execution_result(output=output_array)
        assertion = ExecutionAssertion(execution)
        result = assertion.assert_map_state_output_cardinality(
            input_array=input_array
        )

        assert result.passed is False
        assert len(result.errors) > 0
        error_msg = result.errors[0].message
        # The error should mention both counts
        assert str(n) in error_msg
        assert str(n + 1) in error_msg
