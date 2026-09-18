"""Property-based tests for ASL validation categorization.

# Feature: deployment-integration-tests, Property 3: ASL Validation Categorization

**Validates: Requirements 4.1, 4.2**

For any Step Function ASL definition (valid or invalid), the `validate_asl_definition`
function SHALL return a ValidationResult containing the correct ValidationCategory
(SUCCESS for valid definitions, SYNTAX_ERROR for malformed JSON/invalid state types,
REFERENCE_ERROR for dangling references), the file path of the input, and non-empty
error details for non-SUCCESS categories.
"""

from __future__ import annotations

import string

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.asl_validation.validator import (
    VALID_STATE_TYPES,
    ValidationCategory,
    ValidationResult,
    validate_asl_definition,
)


# ---------------------------------------------------------------------------
# Strategies for generating ASL components
# ---------------------------------------------------------------------------

# Strategy: valid state names (non-empty alphanumeric identifiers)
state_name_st = st.text(
    alphabet=string.ascii_letters + string.digits + "_",
    min_size=1,
    max_size=30,
)


def _terminal_state_def() -> st.SearchStrategy[dict]:
    """Generate a terminal state definition (Succeed or Fail)."""
    return st.one_of(
        st.just({"Type": "Succeed"}),
        st.fixed_dictionaries(
            {"Type": st.just("Fail"), "Error": st.text(min_size=1, max_size=20)}
        ),
    )


def _non_terminal_state_def(next_state: str) -> dict:
    """Generate a non-terminal state definition pointing to next_state."""
    return {"Type": "Task", "Resource": "arn:aws:lambda:us-east-1:123456789012:function:test", "Next": next_state}


@st.composite
def valid_asl_st(draw: st.DrawFn) -> dict:
    """Generate a valid ASL definition that should pass validation.

    Strategy:
    - Generate 1-5 state names
    - Chain them together with Next references
    - The last state is terminal (Succeed or Fail)
    - StartAt points to the first state
    """
    num_states = draw(st.integers(min_value=1, max_value=5))
    # Generate unique state names
    names = draw(
        st.lists(
            state_name_st,
            min_size=num_states,
            max_size=num_states,
            unique=True,
        )
    )

    states: dict = {}
    for i, name in enumerate(names):
        if i == len(names) - 1:
            # Last state is terminal
            states[name] = draw(_terminal_state_def())
        else:
            # Non-terminal state points to the next state in the chain
            states[name] = _non_terminal_state_def(names[i + 1])

    return {
        "StartAt": names[0],
        "States": states,
    }


@st.composite
def valid_asl_with_choice_st(draw: st.DrawFn) -> dict:
    """Generate a valid ASL with a Choice state and valid targets."""
    # At least 3 states: choice + 2 targets
    target_names = draw(
        st.lists(state_name_st, min_size=2, max_size=4, unique=True)
    )
    choice_name = draw(state_name_st.filter(lambda n: n not in target_names))

    choices_list = [
        {
            "Variable": "$.key",
            "StringEquals": f"val_{i}",
            "Next": target_names[i],
        }
        for i in range(len(target_names))
    ]

    states: dict = {
        choice_name: {
            "Type": "Choice",
            "Choices": choices_list,
            "Default": target_names[0],
        }
    }
    for t_name in target_names:
        states[t_name] = {"Type": "Succeed"}

    return {
        "StartAt": choice_name,
        "States": states,
    }


@st.composite
def syntax_error_missing_fields_st(draw: st.DrawFn) -> dict:
    """Generate ASL structures with missing required fields (SYNTAX_ERROR)."""
    variant = draw(st.sampled_from(["no_start_at", "no_states", "empty_states", "states_not_dict"]))

    if variant == "no_start_at":
        # Missing StartAt but has States with at least one valid state
        return {
            "States": {"S1": {"Type": "Succeed"}}
        }
    elif variant == "no_states":
        # Missing States
        return {"StartAt": "S1"}
    elif variant == "empty_states":
        # Empty States dict
        return {"StartAt": "S1", "States": {}}
    else:
        # States is not a dict
        return {"StartAt": "S1", "States": draw(st.sampled_from([[], "string", 123, True]))}


@st.composite
def syntax_error_invalid_type_st(draw: st.DrawFn) -> dict:
    """Generate ASL with invalid state types (SYNTAX_ERROR)."""
    # Generate an invalid type that's not in VALID_STATE_TYPES
    invalid_type = draw(
        st.text(min_size=1, max_size=20).filter(lambda t: t not in VALID_STATE_TYPES)
    )
    state_name = draw(state_name_st)

    return {
        "StartAt": state_name,
        "States": {
            state_name: {"Type": invalid_type, "End": True}
        },
    }


@st.composite
def syntax_error_missing_type_st(draw: st.DrawFn) -> dict:
    """Generate ASL where a state is missing the Type field (SYNTAX_ERROR)."""
    state_name = draw(state_name_st)

    return {
        "StartAt": state_name,
        "States": {
            state_name: {"Resource": "arn:aws:lambda:us-east-1:123456789012:function:f", "End": True}
        },
    }


@st.composite
def syntax_error_state_not_dict_st(draw: st.DrawFn) -> dict:
    """Generate ASL where a state definition is not a dict (SYNTAX_ERROR)."""
    state_name = draw(state_name_st)
    bad_value = draw(st.sampled_from(["string", 42, True, [1, 2, 3]]))

    return {
        "StartAt": state_name,
        "States": {
            state_name: bad_value
        },
    }


@st.composite
def reference_error_start_at_st(draw: st.DrawFn) -> dict:
    """Generate ASL where StartAt references a non-existent state (REFERENCE_ERROR)."""
    actual_name = draw(state_name_st)
    bogus_name = draw(state_name_st.filter(lambda n: n != actual_name))

    return {
        "StartAt": bogus_name,
        "States": {
            actual_name: {"Type": "Succeed"}
        },
    }


@st.composite
def reference_error_next_st(draw: st.DrawFn) -> dict:
    """Generate ASL where a Next field references a non-existent state (REFERENCE_ERROR)."""
    state_name = draw(state_name_st)
    bogus_target = draw(state_name_st.filter(lambda n: n != state_name))

    return {
        "StartAt": state_name,
        "States": {
            state_name: {"Type": "Pass", "Next": bogus_target}
        },
    }


@st.composite
def reference_error_choice_st(draw: st.DrawFn) -> dict:
    """Generate ASL where a Choice branch targets a non-existent state (REFERENCE_ERROR)."""
    choice_name = draw(state_name_st)
    valid_target = draw(state_name_st.filter(lambda n: n != choice_name))
    bogus_target = draw(
        state_name_st.filter(lambda n: n not in (choice_name, valid_target))
    )

    return {
        "StartAt": choice_name,
        "States": {
            choice_name: {
                "Type": "Choice",
                "Choices": [
                    {
                        "Variable": "$.x",
                        "StringEquals": "y",
                        "Next": bogus_target,
                    }
                ],
                "Default": valid_target,
            },
            valid_target: {"Type": "Succeed"},
        },
    }


# Strategy combining all SYNTAX_ERROR generators
syntax_error_st = st.one_of(
    syntax_error_missing_fields_st(),
    syntax_error_invalid_type_st(),
    syntax_error_missing_type_st(),
    syntax_error_state_not_dict_st(),
)

# Strategy combining all REFERENCE_ERROR generators
reference_error_st = st.one_of(
    reference_error_start_at_st(),
    reference_error_next_st(),
    reference_error_choice_st(),
)

# Strategy combining all valid ASL generators
valid_st = st.one_of(
    valid_asl_st(),
    valid_asl_with_choice_st(),
)

# File path strategy
file_path_st = st.text(
    alphabet=string.ascii_letters + string.digits + "/._-",
    min_size=1,
    max_size=100,
)


# ---------------------------------------------------------------------------
# Property Tests
# ---------------------------------------------------------------------------


class TestAslValidationCategorizationProperty:
    """Property 3: ASL Validation Categorization.

    For any Step Function ASL definition (valid or invalid), validate_asl_definition
    SHALL return a ValidationResult with the correct ValidationCategory and non-empty
    error details for non-SUCCESS categories.
    """

    @given(asl=valid_st, file_path=file_path_st)
    @settings(max_examples=100)
    def test_valid_asl_returns_success(self, asl: dict, file_path: str):
        """Valid ASL definitions are categorized as SUCCESS with no errors."""
        result = validate_asl_definition(asl, file_path=file_path)

        assert isinstance(result, ValidationResult)
        assert result.category == ValidationCategory.SUCCESS
        assert result.file_path == file_path
        assert result.errors == []

    @given(asl=syntax_error_st, file_path=file_path_st)
    @settings(max_examples=100)
    def test_syntax_error_asl_returns_syntax_error(self, asl: dict, file_path: str):
        """Malformed ASL definitions (missing fields, invalid types) are categorized
        as SYNTAX_ERROR with non-empty error details."""
        result = validate_asl_definition(asl, file_path=file_path)

        assert isinstance(result, ValidationResult)
        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert result.file_path == file_path
        assert len(result.errors) > 0, "SYNTAX_ERROR must have non-empty error details"

    @given(asl=reference_error_st, file_path=file_path_st)
    @settings(max_examples=100)
    def test_reference_error_asl_returns_reference_error(self, asl: dict, file_path: str):
        """ASL definitions with dangling references are categorized as REFERENCE_ERROR
        with non-empty error details."""
        result = validate_asl_definition(asl, file_path=file_path)

        assert isinstance(result, ValidationResult)
        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert result.file_path == file_path
        assert len(result.errors) > 0, "REFERENCE_ERROR must have non-empty error details"

    @given(
        asl=st.one_of(valid_st, syntax_error_st, reference_error_st),
        file_path=file_path_st,
    )
    @settings(max_examples=100)
    def test_result_always_contains_file_path(self, asl: dict, file_path: str):
        """The file_path is always present in the ValidationResult regardless of category."""
        result = validate_asl_definition(asl, file_path=file_path)

        assert isinstance(result, ValidationResult)
        assert result.file_path == file_path

    @given(asl=st.one_of(syntax_error_st, reference_error_st), file_path=file_path_st)
    @settings(max_examples=100)
    def test_non_success_has_non_empty_errors(self, asl: dict, file_path: str):
        """Any non-SUCCESS result has at least one error message."""
        result = validate_asl_definition(asl, file_path=file_path)

        assert result.category != ValidationCategory.SUCCESS
        assert len(result.errors) > 0, (
            f"Category {result.category.value} must have non-empty errors"
        )
