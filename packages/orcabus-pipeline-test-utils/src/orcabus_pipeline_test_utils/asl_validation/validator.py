"""ASL structural validator.

Validates ASL (Amazon States Language) JSON definitions for:
- Required fields (StartAt, States)
- Valid state types (Task, Pass, Choice, Wait, Succeed, Fail, Parallel, Map)
- Valid transitions (Next fields reference existing states)
- Structural integrity (StartAt references an existing state)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ValidationCategory(Enum):
    """Category of validation result."""

    SUCCESS = "SUCCESS"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    REFERENCE_ERROR = "REFERENCE_ERROR"


@dataclass
class ValidationResult:
    """Result of validating an ASL definition.

    Attributes:
        file_path: Path to the ASL file being validated.
        category: The validation outcome category.
        errors: List of error messages (empty for SUCCESS).
        warnings: List of warning messages.
    """

    file_path: str
    category: ValidationCategory
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# Valid ASL state types per the Amazon States Language specification
VALID_STATE_TYPES = frozenset(
    {"Task", "Pass", "Choice", "Wait", "Succeed", "Fail", "Parallel", "Map"}
)


def validate_asl_definition(
    asl_json: dict,
    file_path: str = "<unknown>",
) -> ValidationResult:
    """Validate an ASL JSON structure for correctness.

    Checks:
    1. Required top-level fields: "StartAt" and "States"
    2. "States" is a non-empty dict
    3. "StartAt" references an existing state
    4. Each state has a valid "Type" field
    5. Terminal states (Succeed, Fail) do not have "Next"
    6. Non-terminal states (except Choice) have valid transitions
    7. State transitions ("Next" fields) reference existing states
    8. Choice state branch targets reference existing states

    Args:
        asl_json: Parsed ASL JSON as a dictionary.
        file_path: Path to the source file (for reporting).

    Returns:
        ValidationResult with category, errors, and warnings.
    """
    errors: list[str] = []
    warnings: list[str] = []
    reference_errors: list[str] = []

    # --- Syntax checks ---

    # Check required top-level fields
    if "StartAt" not in asl_json:
        errors.append("Missing required field: 'StartAt'")

    if "States" not in asl_json:
        errors.append("Missing required field: 'States'")
        # Cannot proceed without States
        return ValidationResult(
            file_path=file_path,
            category=ValidationCategory.SYNTAX_ERROR,
            errors=errors,
            warnings=warnings,
        )

    states = asl_json["States"]

    # States must be a dict
    if not isinstance(states, dict):
        errors.append(
            f"'States' must be an object, got {type(states).__name__}"
        )
        return ValidationResult(
            file_path=file_path,
            category=ValidationCategory.SYNTAX_ERROR,
            errors=errors,
            warnings=warnings,
        )

    # States must not be empty
    if len(states) == 0:
        errors.append("'States' must contain at least one state")

    # Check StartAt references an existing state
    start_at = asl_json.get("StartAt")
    if start_at is not None and start_at not in states:
        reference_errors.append(
            f"'StartAt' references non-existent state: '{start_at}'"
        )

    # Validate each state
    state_names = set(states.keys())
    for state_name, state_def in states.items():
        if not isinstance(state_def, dict):
            errors.append(
                f"State '{state_name}' must be an object, "
                f"got {type(state_def).__name__}"
            )
            continue

        # Check Type field exists and is valid
        if "Type" not in state_def:
            errors.append(f"State '{state_name}' is missing required field: 'Type'")
            continue

        state_type = state_def["Type"]
        if state_type not in VALID_STATE_TYPES:
            errors.append(
                f"State '{state_name}' has invalid type: '{state_type}'. "
                f"Valid types are: {sorted(VALID_STATE_TYPES)}"
            )
            continue

        # Validate transitions based on state type
        _validate_state_transitions(
            state_name=state_name,
            state_def=state_def,
            state_type=state_type,
            state_names=state_names,
            reference_errors=reference_errors,
            warnings=warnings,
        )

    # Determine final category
    if errors:
        return ValidationResult(
            file_path=file_path,
            category=ValidationCategory.SYNTAX_ERROR,
            errors=errors,
            warnings=warnings,
        )

    if reference_errors:
        return ValidationResult(
            file_path=file_path,
            category=ValidationCategory.REFERENCE_ERROR,
            errors=reference_errors,
            warnings=warnings,
        )

    return ValidationResult(
        file_path=file_path,
        category=ValidationCategory.SUCCESS,
        errors=[],
        warnings=warnings,
    )


def _validate_state_transitions(
    state_name: str,
    state_def: dict,
    state_type: str,
    state_names: set[str],
    reference_errors: list[str],
    warnings: list[str],
) -> None:
    """Validate transitions for a single state.

    Args:
        state_name: Name of the state being validated.
        state_def: The state definition dict.
        state_type: The state's Type value.
        state_names: Set of all valid state names in this machine.
        reference_errors: List to append reference errors to.
        warnings: List to append warnings to.
    """
    is_terminal = state_type in ("Succeed", "Fail")
    is_end = state_def.get("End", False)

    # Terminal states (Succeed, Fail) should not have Next
    if is_terminal and "Next" in state_def:
        warnings.append(
            f"State '{state_name}' (type '{state_type}') has a 'Next' field "
            f"which is ignored for terminal states"
        )

    # Check "Next" field references
    if "Next" in state_def and not is_terminal:
        next_state = state_def["Next"]
        if isinstance(next_state, str) and next_state not in state_names:
            reference_errors.append(
                f"State '{state_name}' has 'Next' referencing "
                f"non-existent state: '{next_state}'"
            )

    # Choice states: validate branch targets and Default
    if state_type == "Choice":
        _validate_choice_state(
            state_name=state_name,
            state_def=state_def,
            state_names=state_names,
            reference_errors=reference_errors,
        )

    # Non-terminal, non-Choice states should have either Next or End
    if (
        not is_terminal
        and state_type != "Choice"
        and "Next" not in state_def
        and not is_end
    ):
        warnings.append(
            f"State '{state_name}' (type '{state_type}') has neither "
            f"'Next' nor 'End: true' — this may be intentional if it's "
            f"the last state"
        )

    # Parallel state: validate branch definitions
    if state_type == "Parallel" and "Branches" in state_def:
        _validate_parallel_branches(
            state_name=state_name,
            state_def=state_def,
            reference_errors=reference_errors,
            warnings=warnings,
        )

    # Map state: validate iterator
    if state_type == "Map" and "ItemProcessor" in state_def:
        _validate_map_iterator(
            state_name=state_name,
            state_def=state_def,
            reference_errors=reference_errors,
            warnings=warnings,
        )


def _validate_choice_state(
    state_name: str,
    state_def: dict,
    state_names: set[str],
    reference_errors: list[str],
) -> None:
    """Validate Choice state branch targets and Default.

    Args:
        state_name: Name of the Choice state.
        state_def: The Choice state definition.
        state_names: Set of all valid state names.
        reference_errors: List to append reference errors to.
    """
    # Check Choices array
    choices = state_def.get("Choices", [])
    if isinstance(choices, list):
        for i, choice_rule in enumerate(choices):
            if isinstance(choice_rule, dict) and "Next" in choice_rule:
                target = choice_rule["Next"]
                if isinstance(target, str) and target not in state_names:
                    reference_errors.append(
                        f"State '{state_name}' Choice rule [{i}] "
                        f"has 'Next' referencing non-existent state: '{target}'"
                    )

    # Check Default field
    default_state = state_def.get("Default")
    if isinstance(default_state, str) and default_state not in state_names:
        reference_errors.append(
            f"State '{state_name}' has 'Default' referencing "
            f"non-existent state: '{default_state}'"
        )


def _validate_parallel_branches(
    state_name: str,
    state_def: dict,
    reference_errors: list[str],
    warnings: list[str],
) -> None:
    """Validate Parallel state branch definitions.

    Each branch is itself a mini state machine with StartAt and States.

    Args:
        state_name: Name of the Parallel state.
        state_def: The Parallel state definition.
        reference_errors: List to append reference errors to.
        warnings: List to append warnings to.
    """
    branches = state_def.get("Branches", [])
    if not isinstance(branches, list):
        return

    for i, branch in enumerate(branches):
        if not isinstance(branch, dict):
            continue

        branch_start = branch.get("StartAt")
        branch_states = branch.get("States", {})

        if not isinstance(branch_states, dict):
            continue

        if branch_start is not None and branch_start not in branch_states:
            reference_errors.append(
                f"State '{state_name}' Parallel branch [{i}] "
                f"'StartAt' references non-existent state: '{branch_start}'"
            )


def _validate_map_iterator(
    state_name: str,
    state_def: dict,
    reference_errors: list[str],
    warnings: list[str],
) -> None:
    """Validate Map state iterator/ItemProcessor definitions.

    The ItemProcessor contains a mini state machine.

    Args:
        state_name: Name of the Map state.
        state_def: The Map state definition.
        reference_errors: List to append reference errors to.
        warnings: List to append warnings to.
    """
    item_processor = state_def.get("ItemProcessor", {})
    if not isinstance(item_processor, dict):
        return

    proc_start = item_processor.get("StartAt")
    proc_states = item_processor.get("States", {})

    if not isinstance(proc_states, dict):
        return

    if proc_start is not None and proc_start not in proc_states:
        reference_errors.append(
            f"State '{state_name}' Map ItemProcessor "
            f"'StartAt' references non-existent state: '{proc_start}'"
        )
