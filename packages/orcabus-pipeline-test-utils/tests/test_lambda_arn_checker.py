"""Unit tests for check_lambda_arn_references function."""

import pytest

from orcabus_pipeline_test_utils.asl_validation.reference_checker import (
    check_lambda_arn_references,
)


def _make_asl_with_lambdas(placeholders: list[str]) -> dict:
    """Helper to build an ASL definition containing Lambda ARN placeholders."""
    states = {}
    for i, placeholder in enumerate(placeholders):
        states[f"State{i}"] = {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Arguments": {
                "FunctionName": placeholder,
                "Payload": {"key": "value"},
            },
            "End": True if i == len(placeholders) - 1 else False,
            "Next": f"State{i + 1}" if i < len(placeholders) - 1 else None,
        }
    return {
        "StartAt": "State0",
        "States": states,
    }


def _make_cdk_config(lambdas: dict[str, str]) -> dict:
    """Helper to build a CDK lambda config map.

    Args:
        lambdas: Mapping of lambda_name -> placeholder string.
    """
    return {
        "lambdas": {
            name: {
                "placeholder": placeholder,
                "entry": f"app/lambdas/{name}_py",
            }
            for name, placeholder in lambdas.items()
        }
    }


class TestCheckLambdaArnReferences:
    """Tests for check_lambda_arn_references."""

    def test_no_placeholders_returns_no_errors(self):
        """ASL with no Lambda ARN placeholders produces no errors."""
        asl = {
            "StartAt": "PassState",
            "States": {
                "PassState": {
                    "Type": "Pass",
                    "End": True,
                }
            },
        }
        errors = check_lambda_arn_references(asl, {"lambdas": {}})
        assert errors == []

    def test_all_placeholders_resolved(self):
        """All Lambda ARN placeholders have CDK config entries."""
        asl = _make_asl_with_lambdas([
            "${__calculate_downsampling_ratios_lambda_function_arn__}",
            "${__populate_draft_data_lambda_function_arn__}",
        ])
        cdk_config = _make_cdk_config({
            "calculate_downsampling_ratios": "${__calculate_downsampling_ratios_lambda_function_arn__}",
            "populate_draft_data": "${__populate_draft_data_lambda_function_arn__}",
        })
        errors = check_lambda_arn_references(asl, cdk_config)
        assert errors == []

    def test_unresolved_placeholder_returns_error(self):
        """A Lambda ARN placeholder not in CDK config produces an error."""
        asl = _make_asl_with_lambdas([
            "${__my_missing_lambda_function_arn__}",
        ])
        cdk_config = _make_cdk_config({})
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 1
        assert "${__my_missing_lambda_function_arn__}" in errors[0]

    def test_partial_resolution(self):
        """Some placeholders resolved, some not — errors only for unresolved."""
        asl = _make_asl_with_lambdas([
            "${__get_libraries_lambda_function_arn__}",
            "${__unknown_lambda_function_arn__}",
            "${__another_missing_lambda_function_arn__}",
        ])
        cdk_config = _make_cdk_config({
            "get_libraries": "${__get_libraries_lambda_function_arn__}",
        })
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 2
        # Errors should be sorted
        assert "${__another_missing_lambda_function_arn__}" in errors[0]
        assert "${__unknown_lambda_function_arn__}" in errors[1]

    def test_empty_asl_states(self):
        """An ASL with empty States map produces no errors."""
        asl = {"StartAt": "Start", "States": {}}
        cdk_config = _make_cdk_config({
            "some_function": "${__some_function_lambda_function_arn__}",
        })
        errors = check_lambda_arn_references(asl, cdk_config)
        assert errors == []

    def test_empty_cdk_config(self):
        """Empty CDK config with Lambda placeholders in ASL produces errors."""
        asl = _make_asl_with_lambdas([
            "${__get_workflow_run_object_lambda_function_arn__}",
        ])
        cdk_config = {"lambdas": {}}
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 1

    def test_non_lambda_placeholders_ignored(self):
        """Non-Lambda ARN placeholders (e.g., workflow_name) are not checked."""
        asl = {
            "StartAt": "PassState",
            "States": {
                "PassState": {
                    "Type": "Pass",
                    "Result": {
                        "workflowName": "${__workflow_name__}",
                        "version": "${__default_payload_version__}",
                    },
                    "End": True,
                }
            },
        }
        cdk_config = {"lambdas": {}}
        errors = check_lambda_arn_references(asl, cdk_config)
        assert errors == []

    def test_duplicate_placeholders_counted_once(self):
        """Same placeholder used multiple times produces only one error."""
        asl = _make_asl_with_lambdas([
            "${__repeated_lambda_function_arn__}",
            "${__repeated_lambda_function_arn__}",
        ])
        cdk_config = _make_cdk_config({})
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 1

    def test_missing_lambdas_key_in_config(self):
        """CDK config without 'lambdas' key treats all placeholders as unresolved."""
        asl = _make_asl_with_lambdas([
            "${__my_lambda_function_arn__}",
        ])
        cdk_config = {}  # No "lambdas" key
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 1

    def test_nested_asl_structure(self):
        """Lambda ARN placeholders in deeply nested structures are found."""
        asl = {
            "StartAt": "Parallel",
            "States": {
                "Parallel": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "Branch1Task",
                            "States": {
                                "Branch1Task": {
                                    "Type": "Task",
                                    "Resource": "arn:aws:states:::lambda:invoke",
                                    "Arguments": {
                                        "FunctionName": "${__branch1_lambda_function_arn__}",
                                    },
                                    "End": True,
                                }
                            },
                        },
                        {
                            "StartAt": "Branch2Task",
                            "States": {
                                "Branch2Task": {
                                    "Type": "Task",
                                    "Resource": "arn:aws:states:::lambda:invoke",
                                    "Arguments": {
                                        "FunctionName": "${__branch2_lambda_function_arn__}",
                                    },
                                    "End": True,
                                }
                            },
                        },
                    ],
                    "End": True,
                }
            },
        }
        cdk_config = _make_cdk_config({
            "branch1": "${__branch1_lambda_function_arn__}",
        })
        errors = check_lambda_arn_references(asl, cdk_config)
        assert len(errors) == 1
        assert "${__branch2_lambda_function_arn__}" in errors[0]

    def test_realistic_cdk_config_structure(self):
        """Validates against the real CDK config format from the design doc."""
        asl = _make_asl_with_lambdas([
            "${__calculate_downsampling_ratios_lambda_function_arn__}",
            "${__populate_draft_data_lambda_function_arn__}",
        ])
        cdk_config = {
            "lambdas": {
                "calculate_downsampling_ratios": {
                    "placeholder": "${__calculate_downsampling_ratios_lambda_function_arn__}",
                    "entry": "app/lambdas/calculate_downsampling_ratios_py",
                },
                "populate_draft_data": {
                    "placeholder": "${__populate_draft_data_lambda_function_arn__}",
                    "entry": "app/lambdas/populate_draft_data_py",
                },
            }
        }
        errors = check_lambda_arn_references(asl, cdk_config)
        assert errors == []
