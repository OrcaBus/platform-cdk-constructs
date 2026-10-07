"""Property-based tests for state reference resolution.

# Feature: deployment-integration-tests, Property 4: State Reference Resolution

Validates: Requirements 4.3

For any ASL definition JSON containing "Next", "Default", and Choice branch target
fields, the `check_state_references` function SHALL return an error for every target
value that does not exist as a key in the "States" map, and SHALL return no errors
when all targets reference existing states.
"""

from __future__ import annotations

import hypothesis
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.asl_validation.reference_checker import (
    check_state_references,
)


# --- Strategies ---

# Generate valid state names (non-empty, alphanumeric with limited special chars)
state_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=1,
    max_size=30,
).filter(lambda s: s.strip() != "")


def _build_asl_all_valid(state_names: list[str]) -> dict:
    """Build an ASL definition where all references are valid.

    Creates a linear chain of Task states ending with a Succeed state.
    All Next references point to the subsequent state in the chain.
    """
    if len(state_names) < 2:
        return {
            "StartAt": state_names[0],
            "States": {state_names[0]: {"Type": "Succeed"}},
        }

    states = {}
    for i, name in enumerate(state_names[:-1]):
        states[name] = {"Type": "Task", "Next": state_names[i + 1]}
    states[state_names[-1]] = {"Type": "Succeed"}

    return {"StartAt": state_names[0], "States": states}


def _build_asl_with_choice_all_valid(
    state_names: list[str],
    choice_state_name: str,
    branch_targets: list[str],
    default_target: str,
) -> dict:
    """Build an ASL with a Choice state where all targets are valid.

    All branch_targets and default_target must be in state_names.
    """
    states = {}
    # Choice state
    choices = [
        {"Variable": "$.x", "NumericEquals": i, "Next": target}
        for i, target in enumerate(branch_targets)
    ]
    states[choice_state_name] = {
        "Type": "Choice",
        "Choices": choices,
        "Default": default_target,
    }
    # All referenced states as Succeed
    for name in state_names:
        if name != choice_state_name:
            states[name] = {"Type": "Succeed"}

    return {"StartAt": choice_state_name, "States": states}


@st.composite
def valid_linear_asl(draw: st.DrawFn) -> dict:
    """Strategy to generate a valid linear ASL definition with no dangling references."""
    num_states = draw(st.integers(min_value=2, max_value=10))
    names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_states,
            max_size=num_states,
            unique=True,
        )
    )
    return _build_asl_all_valid(names)


@st.composite
def valid_choice_asl(draw: st.DrawFn) -> dict:
    """Strategy to generate a valid ASL with Choice state, all targets valid."""
    num_targets = draw(st.integers(min_value=1, max_value=5))
    # Generate unique state names: choice state + target states
    all_names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_targets + 2,
            max_size=num_targets + 5,
            unique=True,
        )
    )
    choice_name = all_names[0]
    # Pick branch targets and default from the remaining names
    remaining = all_names[1:]
    branch_targets = remaining[:num_targets]
    default_target = remaining[-1]

    return _build_asl_with_choice_all_valid(
        state_names=all_names,
        choice_state_name=choice_name,
        branch_targets=branch_targets,
        default_target=default_target,
    )


@st.composite
def asl_with_dangling_next(draw: st.DrawFn) -> tuple[dict, set[str]]:
    """Strategy to generate an ASL with some dangling Next references.

    Returns the ASL and the set of dangling target names that are actually
    referenced in the ASL's Next fields.
    """
    num_valid = draw(st.integers(min_value=2, max_value=6))
    num_dangling = draw(st.integers(min_value=1, max_value=4))

    valid_names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_valid,
            max_size=num_valid,
            unique=True,
        )
    )
    # Generate dangling names that are NOT in valid_names
    dangling_names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_dangling,
            max_size=num_dangling,
            unique=True,
        )
    )
    # Ensure dangling names are truly not in the valid set
    dangling_names = [n for n in dangling_names if n not in valid_names]
    assume(len(dangling_names) >= 1)

    states = {}
    actually_referenced_dangling = set()

    # First state references a dangling target
    states[valid_names[0]] = {"Type": "Task", "Next": dangling_names[0]}
    actually_referenced_dangling.add(dangling_names[0])

    # Remaining valid states — some get dangling Next, others are Succeed
    for i, name in enumerate(valid_names[1:], start=1):
        dangling_idx = i  # offset into dangling_names (skip index 0, already used)
        if dangling_idx < len(dangling_names):
            states[name] = {"Type": "Task", "Next": dangling_names[dangling_idx]}
            actually_referenced_dangling.add(dangling_names[dangling_idx])
        else:
            states[name] = {"Type": "Succeed"}

    asl = {"StartAt": valid_names[0], "States": states}

    return asl, actually_referenced_dangling


@st.composite
def asl_with_dangling_default(draw: st.DrawFn) -> tuple[dict, str]:
    """Strategy to generate an ASL with a Choice state that has a dangling Default.

    Returns the ASL and the dangling default target name.
    """
    num_states = draw(st.integers(min_value=2, max_value=6))
    names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_states,
            max_size=num_states,
            unique=True,
        )
    )
    dangling_default = draw(state_name_strategy)
    assume(dangling_default not in names)

    choice_name = names[0]
    # Valid branch targets from remaining names
    branch_target = names[1]

    states = {}
    states[choice_name] = {
        "Type": "Choice",
        "Choices": [
            {"Variable": "$.x", "NumericEquals": 1, "Next": branch_target},
        ],
        "Default": dangling_default,
    }
    for name in names[1:]:
        states[name] = {"Type": "Succeed"}

    asl = {"StartAt": choice_name, "States": states}
    return asl, dangling_default


@st.composite
def asl_with_dangling_choice_branch(draw: st.DrawFn) -> tuple[dict, str]:
    """Strategy to generate an ASL with a Choice state that has a dangling branch target.

    Returns the ASL and the dangling branch target name.
    """
    num_states = draw(st.integers(min_value=2, max_value=6))
    names = draw(
        st.lists(
            state_name_strategy,
            min_size=num_states,
            max_size=num_states,
            unique=True,
        )
    )
    dangling_branch = draw(state_name_strategy)
    assume(dangling_branch not in names)

    choice_name = names[0]
    valid_default = names[1]

    states = {}
    states[choice_name] = {
        "Type": "Choice",
        "Choices": [
            {"Variable": "$.x", "NumericEquals": 1, "Next": dangling_branch},
        ],
        "Default": valid_default,
    }
    for name in names[1:]:
        states[name] = {"Type": "Succeed"}

    asl = {"StartAt": choice_name, "States": states}
    return asl, dangling_branch


# --- Property Tests ---


class TestPropertyStateReferenceResolution:
    """Property-based tests for check_state_references.

    **Validates: Requirements 4.3**
    """

    @settings(max_examples=100)
    @given(asl=valid_linear_asl())
    def test_no_errors_for_valid_linear_workflow(self, asl: dict):
        """When all Next references point to existing states, no errors are returned."""
        errors = check_state_references(asl)
        assert errors == [], f"Expected no errors for valid ASL, got: {errors}"

    @settings(max_examples=100)
    @given(asl=valid_choice_asl())
    def test_no_errors_for_valid_choice_workflow(self, asl: dict):
        """When all Choice branch targets and Default point to existing states, no errors."""
        errors = check_state_references(asl)
        assert errors == [], f"Expected no errors for valid Choice ASL, got: {errors}"

    @settings(max_examples=100)
    @given(data=asl_with_dangling_next())
    def test_errors_for_dangling_next_targets(self, data: tuple[dict, set[str]]):
        """Every Next target not in the States map produces an error."""
        asl, expected_dangling = data
        errors = check_state_references(asl)

        # Each dangling target must be mentioned in at least one error
        for dangling_name in expected_dangling:
            matching_errors = [e for e in errors if dangling_name in e]
            assert len(matching_errors) >= 1, (
                f"Expected error for dangling target '{dangling_name}' but found none "
                f"in errors: {errors}"
            )

    @settings(max_examples=100)
    @given(data=asl_with_dangling_default())
    def test_errors_for_dangling_default_target(self, data: tuple[dict, str]):
        """A Default target not in the States map produces an error."""
        asl, dangling_default = data
        errors = check_state_references(asl)

        matching_errors = [e for e in errors if dangling_default in e]
        assert len(matching_errors) >= 1, (
            f"Expected error for dangling Default target '{dangling_default}' "
            f"but found none in errors: {errors}"
        )

    @settings(max_examples=100)
    @given(data=asl_with_dangling_choice_branch())
    def test_errors_for_dangling_choice_branch_target(self, data: tuple[dict, str]):
        """A Choice branch Next target not in the States map produces an error."""
        asl, dangling_branch = data
        errors = check_state_references(asl)

        matching_errors = [e for e in errors if dangling_branch in e]
        assert len(matching_errors) >= 1, (
            f"Expected error for dangling Choice branch target '{dangling_branch}' "
            f"but found none in errors: {errors}"
        )

    @settings(max_examples=100)
    @given(asl=valid_linear_asl())
    def test_no_false_positives_for_valid_states(self, asl: dict):
        """Valid state names never appear as targets in error messages."""
        errors = check_state_references(asl)
        # If there are any errors, they should not reference valid states as dangling
        defined_states = set(asl.get("States", {}).keys())
        for error in errors:
            # No valid state should be reported as undefined
            for state_name in defined_states:
                assert f"undefined state '{state_name}'" not in error
