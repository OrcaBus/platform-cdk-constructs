"""Property-based test for Lambda ARN Placeholder Cross-Reference.

# Feature: deployment-integration-tests, Property 5: Lambda ARN Placeholder Cross-Reference

**Validates: Requirements 4.4**

Property 5: For any ASL definition containing Lambda ARN placeholders and any CDK
lambda configuration map, the check_lambda_arn_references function SHALL return an
error for every placeholder in the ASL that has no corresponding entry in the config
map, and SHALL return no errors when all placeholders are present in the config map.
"""

from __future__ import annotations

import json

from hypothesis import given, settings
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.asl_validation.reference_checker import (
    check_lambda_arn_references,
)


# --- Strategies ---

# Generate valid lambda names: lowercase letters and underscores, 1-30 chars
lambda_name_strategy = st.from_regex(r"[a-z][a-z0-9_]{0,29}", fullmatch=True)


def lambda_placeholder(name: str) -> str:
    """Build a Lambda ARN placeholder string from a name."""
    return f"${{__{name}_lambda_function_arn__}}"


def make_asl_with_placeholders(placeholder_names: list[str]) -> dict:
    """Build a minimal ASL definition that uses the given Lambda ARN placeholders."""
    if not placeholder_names:
        return {
            "StartAt": "PassState",
            "States": {
                "PassState": {
                    "Type": "Pass",
                    "End": True,
                }
            },
        }

    states = {}
    for i, name in enumerate(placeholder_names):
        is_last = i == len(placeholder_names) - 1
        state_def: dict = {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Arguments": {
                "FunctionName": lambda_placeholder(name),
                "Payload": {"key": "value"},
            },
        }
        if is_last:
            state_def["End"] = True
        else:
            state_def["Next"] = f"State{i + 1}"
        states[f"State{i}"] = state_def

    return {
        "StartAt": "State0",
        "States": states,
    }


def make_cdk_config(names: list[str]) -> dict:
    """Build a CDK lambda config map for the given lambda names."""
    return {
        "lambdas": {
            name: {
                "placeholder": lambda_placeholder(name),
                "entry": f"app/lambdas/{name}_py",
            }
            for name in names
        }
    }


@settings(max_examples=100)
@given(
    asl_names=st.lists(lambda_name_strategy, min_size=0, max_size=10, unique=True),
    config_names=st.lists(lambda_name_strategy, min_size=0, max_size=10, unique=True),
)
def test_lambda_arn_cross_reference_errors_for_missing_placeholders(
    asl_names: list[str],
    config_names: list[str],
) -> None:
    """Property 5: errors for placeholders missing from config, no errors when all present.

    For any set of Lambda ARN placeholders in an ASL definition and any CDK config map:
    - Every placeholder in the ASL that has NO corresponding entry in the config
      SHALL produce an error.
    - When all placeholders ARE present in the config map, there SHALL be no errors.
    """
    asl_json = make_asl_with_placeholders(asl_names)
    cdk_config = make_cdk_config(config_names)

    errors = check_lambda_arn_references(asl_json, cdk_config)

    # Determine which ASL placeholders are missing from the config
    config_placeholder_set = {lambda_placeholder(n) for n in config_names}
    asl_placeholder_set = {lambda_placeholder(n) for n in asl_names}

    missing_placeholders = asl_placeholder_set - config_placeholder_set

    # The number of errors should equal the number of missing placeholders
    assert len(errors) == len(missing_placeholders), (
        f"Expected {len(missing_placeholders)} errors for missing placeholders, "
        f"got {len(errors)}. "
        f"ASL placeholders: {asl_placeholder_set}, "
        f"Config placeholders: {config_placeholder_set}, "
        f"Errors: {errors}"
    )

    # Each missing placeholder should appear in exactly one error message
    for placeholder in missing_placeholders:
        matching_errors = [e for e in errors if placeholder in e]
        assert len(matching_errors) == 1, (
            f"Expected exactly one error mentioning '{placeholder}', "
            f"got {len(matching_errors)}. Errors: {errors}"
        )

    # No error should mention a placeholder that IS in the config
    present_placeholders = asl_placeholder_set & config_placeholder_set
    for placeholder in present_placeholders:
        matching_errors = [e for e in errors if placeholder in e]
        assert len(matching_errors) == 0, (
            f"Placeholder '{placeholder}' is in config but appears in error: "
            f"{matching_errors}"
        )


@settings(max_examples=100)
@given(
    names=st.lists(lambda_name_strategy, min_size=1, max_size=10, unique=True),
)
def test_lambda_arn_no_errors_when_all_present(names: list[str]) -> None:
    """When all ASL placeholders are present in the config, no errors are returned."""
    asl_json = make_asl_with_placeholders(names)
    cdk_config = make_cdk_config(names)

    errors = check_lambda_arn_references(asl_json, cdk_config)

    assert errors == [], (
        f"Expected no errors when all placeholders are in config, "
        f"but got: {errors}"
    )


@settings(max_examples=100)
@given(
    asl_names=st.lists(lambda_name_strategy, min_size=1, max_size=10, unique=True),
)
def test_lambda_arn_all_errors_when_config_empty(asl_names: list[str]) -> None:
    """When config is empty, every ASL placeholder produces an error."""
    asl_json = make_asl_with_placeholders(asl_names)
    cdk_config = make_cdk_config([])

    errors = check_lambda_arn_references(asl_json, cdk_config)

    assert len(errors) == len(asl_names), (
        f"Expected {len(asl_names)} errors for all-missing placeholders, "
        f"got {len(errors)}. Errors: {errors}"
    )
