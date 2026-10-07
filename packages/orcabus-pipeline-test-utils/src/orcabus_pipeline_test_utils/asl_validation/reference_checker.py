"""State and Lambda ARN reference checker.

Validates that:
- All state references (Next, Default, Choice targets) resolve to defined states
- All Lambda ARN placeholders correspond to CDK-defined functions
"""

from __future__ import annotations

import json
import re
from typing import Any

# Regex to match ${__xxx_lambda_function_arn__} placeholders
LAMBDA_ARN_PLACEHOLDER_PATTERN = re.compile(
    r"\$\{__([a-z0-9_]+_lambda_function_arn)__\}"
)


def check_state_references(asl_json: dict) -> list[str]:
    """Verify all 'Next', 'Default', and Choice branch targets reference existing states.

    Walks the entire ASL definition and checks that every state reference
    (via "Next" fields, "Default" fields in Choice states, and Choice rule
    branch targets) points to a state that exists in the top-level "States" map.

    Also verifies the "StartAt" field references an existing state.

    Args:
        asl_json: Parsed ASL JSON definition as a dictionary. Expected to
            contain "States" (dict) and optionally "StartAt" (str) at the
            top level.

    Returns:
        List of error strings describing dangling references. Empty list
        means all references are valid.
    """
    errors: list[str] = []

    states = asl_json.get("States", {})
    if not isinstance(states, dict):
        errors.append("'States' field is not a valid object")
        return errors

    defined_state_names = set(states.keys())

    # Check StartAt
    start_at = asl_json.get("StartAt")
    if isinstance(start_at, str) and start_at not in defined_state_names:
        errors.append(
            f"'StartAt' references undefined state '{start_at}'"
        )

    # Walk each state and collect reference errors
    for state_name, state_def in states.items():
        if not isinstance(state_def, dict):
            continue

        state_errors = _check_state_def_references(
            state_name, state_def, defined_state_names
        )
        errors.extend(state_errors)

    return errors


def _check_state_def_references(
    state_name: str,
    state_def: dict,
    defined_state_names: set[str],
) -> list[str]:
    """Check references within a single state definition.

    Args:
        state_name: Name of the state being checked (for error messages).
        state_def: The state definition dictionary.
        defined_state_names: Set of all valid state names.

    Returns:
        List of error strings for this state.
    """
    errors: list[str] = []

    # Check "Next" field (present in Task, Pass, Wait, Parallel, Map states)
    next_state = state_def.get("Next")
    if isinstance(next_state, str) and next_state not in defined_state_names:
        errors.append(
            f"State '{state_name}' has 'Next' referencing undefined state '{next_state}'"
        )

    # Check "Default" field (present in Choice states)
    default_state = state_def.get("Default")
    if isinstance(default_state, str) and default_state not in defined_state_names:
        errors.append(
            f"State '{state_name}' has 'Default' referencing undefined state '{default_state}'"
        )

    # Check Choice state rules (Choices array with "Next" in each rule)
    choices = state_def.get("Choices")
    if isinstance(choices, list):
        for i, rule in enumerate(choices):
            if not isinstance(rule, dict):
                continue
            rule_next = rule.get("Next")
            if isinstance(rule_next, str) and rule_next not in defined_state_names:
                errors.append(
                    f"State '{state_name}' Choice rule [{i}] has 'Next' "
                    f"referencing undefined state '{rule_next}'"
                )

    # Check Catch blocks (can reference states via "Next")
    catch_blocks = state_def.get("Catch")
    if isinstance(catch_blocks, list):
        for i, catch_block in enumerate(catch_blocks):
            if not isinstance(catch_block, dict):
                continue
            catch_next = catch_block.get("Next")
            if isinstance(catch_next, str) and catch_next not in defined_state_names:
                errors.append(
                    f"State '{state_name}' Catch [{i}] has 'Next' "
                    f"referencing undefined state '{catch_next}'"
                )

    # Check nested states in Parallel branches
    branches = state_def.get("Branches")
    if isinstance(branches, list):
        for i, branch in enumerate(branches):
            if not isinstance(branch, dict):
                continue
            # Each branch has its own States map — validate internally
            branch_errors = _check_branch_references(
                state_name, i, branch
            )
            errors.extend(branch_errors)

    # Check Map state iterator/item processor
    iterator = state_def.get("Iterator") or state_def.get("ItemProcessor")
    if isinstance(iterator, dict):
        branch_errors = _check_branch_references(
            state_name, "Iterator", iterator
        )
        errors.extend(branch_errors)

    return errors


def _check_branch_references(
    parent_state_name: str,
    branch_index: int | str,
    branch_def: dict,
) -> list[str]:
    """Check references within a Parallel branch or Map iterator.

    Branches have their own "States" map, so references are validated
    against that local scope.

    Args:
        parent_state_name: Name of the parent Parallel/Map state.
        branch_index: Index or label of the branch.
        branch_def: The branch definition with its own "States" and "StartAt".

    Returns:
        List of error strings for this branch.
    """
    errors: list[str] = []
    branch_states = branch_def.get("States", {})

    if not isinstance(branch_states, dict):
        return errors

    branch_state_names = set(branch_states.keys())

    # Check branch StartAt
    start_at = branch_def.get("StartAt")
    if isinstance(start_at, str) and start_at not in branch_state_names:
        errors.append(
            f"State '{parent_state_name}' branch [{branch_index}] 'StartAt' "
            f"references undefined state '{start_at}'"
        )

    # Recursively check each state in the branch
    for state_name, state_def in branch_states.items():
        if not isinstance(state_def, dict):
            continue
        state_errors = _check_state_def_references(
            f"{parent_state_name}.branch[{branch_index}].{state_name}",
            state_def,
            branch_state_names,
        )
        errors.extend(state_errors)

    return errors


def check_lambda_arn_references(
    asl_json: dict,
    cdk_lambda_config: dict[str, Any],
) -> list[str]:
    """Verify Lambda ARN placeholders correspond to CDK-defined functions.

    Scans the ASL definition for all ${__xxx_lambda_function_arn__} placeholders
    and checks that each one has a corresponding entry in the CDK lambda
    configuration map.

    Args:
        asl_json: Parsed ASL definition as a dictionary.
        cdk_lambda_config: CDK lambda configuration map with structure:
            {
                "lambdas": {
                    "<lambda_name>": {
                        "placeholder": "${__<name>_lambda_function_arn__}",
                        "entry": "app/lambdas/<name>_py"
                    }
                }
            }

    Returns:
        List of error strings for unresolved placeholders. Empty if all valid.
    """
    # Extract all known placeholders from the CDK config
    known_placeholders: set[str] = set()
    lambdas_config = cdk_lambda_config.get("lambdas", {})
    for lambda_name, lambda_info in lambdas_config.items():
        if isinstance(lambda_info, dict) and "placeholder" in lambda_info:
            known_placeholders.add(lambda_info["placeholder"])

    # Find all Lambda ARN placeholders in the ASL definition
    asl_str = json.dumps(asl_json)
    found_placeholders = set(LAMBDA_ARN_PLACEHOLDER_PATTERN.findall(asl_str))

    # Check each found placeholder against the known set
    errors: list[str] = []
    for inner_name in sorted(found_placeholders):
        full_placeholder = f"${{__{inner_name}__}}"
        if full_placeholder not in known_placeholders:
            errors.append(
                f"Lambda ARN placeholder '{full_placeholder}' in ASL definition "
                f"has no corresponding entry in the CDK lambda configuration"
            )

    return errors
