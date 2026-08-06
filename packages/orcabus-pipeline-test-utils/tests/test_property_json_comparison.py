"""Property-based tests for JSONata output comparison (match_json).

# Feature: deployment-integration-tests, Property 9: JSONata Output Comparison

**Validates: Requirements 6.4**

For any pair of JSON values (actual output from JSONata evaluation and expected output),
the comparison logic SHALL return pass when the values are structurally equal (respecting
wildcard placeholders like `{% any_string %}`) and fail when they differ.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.sfn_local.assertions import (
    ANY_STRING_PLACEHOLDER,
    match_json,
)


# ---------------------------------------------------------------------------
# Strategies for generating JSON values
# ---------------------------------------------------------------------------

# Strategy for JSON scalar values (no wildcard)
json_scalars = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
    st.text(min_size=0, max_size=30),
)


def json_values_st(max_depth: int = 3) -> st.SearchStrategy:
    """Generate arbitrary JSON-compatible values up to a given depth."""
    if max_depth <= 0:
        return json_scalars
    return st.one_of(
        json_scalars,
        st.lists(json_values_st(max_depth - 1), max_size=4),
        st.dictionaries(
            keys=st.text(min_size=1, max_size=10),
            values=json_values_st(max_depth - 1),
            max_size=4,
        ),
    )


# Strategy for non-empty strings (used as actual values matching wildcards)
non_empty_strings = st.text(min_size=1, max_size=30)


@st.composite
def json_with_wildcards_st(draw: st.DrawFn) -> tuple:
    """Generate a pair of (actual, expected) JSON values where expected may contain wildcards.

    Returns (actual, expected) such that actual matches expected (respecting wildcards).
    """
    # Decide the structure type
    structure = draw(st.sampled_from(["scalar", "dict", "list", "nested_dict"]))

    if structure == "scalar":
        # Either exact match or wildcard
        use_wildcard = draw(st.booleans())
        if use_wildcard:
            actual_val = draw(non_empty_strings)
            return (actual_val, ANY_STRING_PLACEHOLDER)
        else:
            val = draw(json_scalars)
            return (val, val)

    elif structure == "dict":
        # Generate a dict with some wildcard fields
        num_keys = draw(st.integers(min_value=1, max_value=5))
        keys = draw(
            st.lists(
                st.text(min_size=1, max_size=10),
                min_size=num_keys,
                max_size=num_keys,
                unique=True,
            )
        )
        actual_dict: dict = {}
        expected_dict: dict = {}
        for key in keys:
            use_wildcard = draw(st.booleans())
            if use_wildcard:
                actual_dict[key] = draw(non_empty_strings)
                expected_dict[key] = ANY_STRING_PLACEHOLDER
            else:
                val = draw(json_scalars)
                actual_dict[key] = val
                expected_dict[key] = val
        return (actual_dict, expected_dict)

    elif structure == "list":
        # Generate a list with some wildcard elements
        num_items = draw(st.integers(min_value=0, max_value=5))
        actual_list: list = []
        expected_list: list = []
        for _ in range(num_items):
            use_wildcard = draw(st.booleans())
            if use_wildcard:
                actual_list.append(draw(non_empty_strings))
                expected_list.append(ANY_STRING_PLACEHOLDER)
            else:
                val = draw(json_scalars)
                actual_list.append(val)
                expected_list.append(val)
        return (actual_list, expected_list)

    else:  # nested_dict
        # Generate a nested dict with wildcards at leaf level
        outer_keys = draw(
            st.lists(
                st.text(min_size=1, max_size=8),
                min_size=1,
                max_size=3,
                unique=True,
            )
        )
        actual_outer: dict = {}
        expected_outer: dict = {}
        for okey in outer_keys:
            inner_keys = draw(
                st.lists(
                    st.text(min_size=1, max_size=8),
                    min_size=1,
                    max_size=3,
                    unique=True,
                )
            )
            actual_inner: dict = {}
            expected_inner: dict = {}
            for ikey in inner_keys:
                use_wildcard = draw(st.booleans())
                if use_wildcard:
                    actual_inner[ikey] = draw(non_empty_strings)
                    expected_inner[ikey] = ANY_STRING_PLACEHOLDER
                else:
                    val = draw(json_scalars)
                    actual_inner[ikey] = val
                    expected_inner[ikey] = val
            actual_outer[okey] = actual_inner
            expected_outer[okey] = expected_inner
        return (actual_outer, expected_outer)


@st.composite
def mismatched_json_pair_st(draw: st.DrawFn) -> tuple:
    """Generate a pair of (actual, expected) JSON values that differ structurally.

    Returns (actual, expected) where match_json should report errors.
    """
    mismatch_type = draw(
        st.sampled_from([
            "scalar_value_mismatch",
            "missing_key",
            "extra_key",
            "type_mismatch",
            "array_length_mismatch",
            "wildcard_non_string",
            "nested_mismatch",
        ])
    )

    if mismatch_type == "scalar_value_mismatch":
        val1 = draw(json_scalars)
        val2 = draw(json_scalars.filter(lambda v: v != val1))
        return (val1, val2)

    elif mismatch_type == "missing_key":
        # actual has fewer keys than expected
        key1 = draw(st.text(min_size=1, max_size=10))
        key2 = draw(st.text(min_size=1, max_size=10).filter(lambda k: k != key1))
        val = draw(json_scalars)
        actual = {key1: val}
        expected = {key1: val, key2: draw(json_scalars)}
        return (actual, expected)

    elif mismatch_type == "extra_key":
        # actual has more keys than expected
        key1 = draw(st.text(min_size=1, max_size=10))
        key2 = draw(st.text(min_size=1, max_size=10).filter(lambda k: k != key1))
        val = draw(json_scalars)
        actual = {key1: val, key2: draw(json_scalars)}
        expected = {key1: val}
        return (actual, expected)

    elif mismatch_type == "type_mismatch":
        # actual is a different JSON type than expected
        variant = draw(st.sampled_from(["dict_vs_list", "list_vs_dict", "scalar_vs_dict"]))
        if variant == "dict_vs_list":
            actual = [1, 2, 3]
            expected = {"key": "value"}
            return (actual, expected)
        elif variant == "list_vs_dict":
            actual = {"key": "value"}
            expected = [1, 2, 3]
            return (actual, expected)
        else:
            actual = draw(st.integers())
            expected = {"key": "value"}
            return (actual, expected)

    elif mismatch_type == "array_length_mismatch":
        # Arrays of different lengths
        len1 = draw(st.integers(min_value=0, max_value=5))
        len2 = draw(st.integers(min_value=0, max_value=5).filter(lambda l: l != len1))
        actual = [draw(json_scalars) for _ in range(len1)]
        expected = [draw(json_scalars) for _ in range(len2)]
        return (actual, expected)

    elif mismatch_type == "wildcard_non_string":
        # Wildcard expects a string but actual is not a string
        non_string_val = draw(
            st.one_of(
                st.integers(),
                st.booleans(),
                st.none(),
                st.lists(st.integers(), max_size=3),
                st.dictionaries(st.text(min_size=1, max_size=5), st.integers(), max_size=2),
            )
        )
        return (non_string_val, ANY_STRING_PLACEHOLDER)

    else:  # nested_mismatch
        # Nested dict where an inner value differs
        key = draw(st.text(min_size=1, max_size=10))
        inner_key = draw(st.text(min_size=1, max_size=10))
        val1 = draw(st.text(min_size=1, max_size=10))
        val2 = draw(st.text(min_size=1, max_size=10).filter(lambda v: v != val1))
        actual = {key: {inner_key: val1}}
        expected = {key: {inner_key: val2}}
        return (actual, expected)


# ---------------------------------------------------------------------------
# Property Tests
# ---------------------------------------------------------------------------


class TestJsonataOutputComparisonProperty:
    """Property 9: JSONata Output Comparison.

    For any pair of JSON values (actual output and expected output), the comparison
    logic SHALL return pass when the values are structurally equal (respecting wildcard
    placeholders like `{% any_string %}`) and fail when they differ.
    """

    @given(pair=json_with_wildcards_st())
    @settings(max_examples=100)
    def test_structurally_equal_values_return_no_errors(self, pair: tuple):
        """When actual matches expected (respecting wildcards), match_json returns
        an empty error list (pass)."""
        actual, expected = pair
        errors = match_json(actual, expected)
        assert errors == [], (
            f"Expected no errors for matching pair but got: {errors}\n"
            f"actual={actual!r}, expected={expected!r}"
        )

    @given(pair=mismatched_json_pair_st())
    @settings(max_examples=100)
    def test_structurally_different_values_return_errors(self, pair: tuple):
        """When actual differs from expected, match_json returns a non-empty error list (fail)."""
        actual, expected = pair
        errors = match_json(actual, expected)
        assert len(errors) > 0, (
            f"Expected errors for mismatched pair but got none.\n"
            f"actual={actual!r}, expected={expected!r}"
        )

    @given(value=json_values_st(max_depth=3))
    @settings(max_examples=100)
    def test_value_matches_itself(self, value):
        """Any JSON value compared against itself returns no errors (reflexivity)."""
        errors = match_json(value, value)
        assert errors == [], (
            f"Expected no errors for self-comparison but got: {errors}\n"
            f"value={value!r}"
        )

    @given(actual_str=non_empty_strings)
    @settings(max_examples=100)
    def test_wildcard_matches_any_string(self, actual_str: str):
        """The wildcard placeholder matches any string value."""
        errors = match_json(actual_str, ANY_STRING_PLACEHOLDER)
        assert errors == [], (
            f"Wildcard should match any string, but got errors: {errors}\n"
            f"actual_str={actual_str!r}"
        )

    @given(
        non_string=st.one_of(
            st.integers(),
            st.booleans(),
            st.none(),
            st.lists(st.integers(), max_size=3),
            st.dictionaries(st.text(min_size=1, max_size=5), st.integers(), max_size=2),
        )
    )
    @settings(max_examples=100)
    def test_wildcard_rejects_non_string(self, non_string):
        """The wildcard placeholder fails when actual is not a string."""
        errors = match_json(non_string, ANY_STRING_PLACEHOLDER)
        assert len(errors) > 0, (
            f"Wildcard should reject non-string values but got no errors.\n"
            f"non_string={non_string!r}"
        )
