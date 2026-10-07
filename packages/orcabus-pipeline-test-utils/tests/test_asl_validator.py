"""Unit tests for the ASL structural validator."""

import pytest

from orcabus_pipeline_test_utils.asl_validation.validator import (
    VALID_STATE_TYPES,
    ValidationCategory,
    ValidationResult,
    validate_asl_definition,
)


class TestValidateAslDefinition:
    """Tests for validate_asl_definition."""

    def test_valid_simple_state_machine(self):
        """A minimal valid state machine returns SUCCESS."""
        asl = {
            "StartAt": "MyTask",
            "States": {
                "MyTask": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:my-fn",
                    "End": True,
                }
            },
        }
        result = validate_asl_definition(asl, file_path="test.asl.json")

        assert result.category == ValidationCategory.SUCCESS
        assert result.file_path == "test.asl.json"
        assert result.errors == []

    def test_valid_multi_state_machine(self):
        """A multi-state machine with valid transitions returns SUCCESS."""
        asl = {
            "StartAt": "First",
            "States": {
                "First": {"Type": "Pass", "Next": "Second"},
                "Second": {"Type": "Task", "Resource": "arn:aws:...", "Next": "Third"},
                "Third": {"Type": "Succeed"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS
        assert result.errors == []

    def test_missing_start_at(self):
        """Missing StartAt returns SYNTAX_ERROR."""
        asl = {
            "States": {
                "MyTask": {"Type": "Task", "Resource": "...", "End": True}
            }
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("StartAt" in e for e in result.errors)

    def test_missing_states(self):
        """Missing States returns SYNTAX_ERROR."""
        asl = {"StartAt": "MyTask"}
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("States" in e for e in result.errors)

    def test_states_not_a_dict(self):
        """States that is not a dict returns SYNTAX_ERROR."""
        asl = {"StartAt": "MyTask", "States": ["not", "a", "dict"]}
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("object" in e for e in result.errors)

    def test_empty_states(self):
        """Empty States dict returns SYNTAX_ERROR."""
        asl = {"StartAt": "MyTask", "States": {}}
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("at least one state" in e for e in result.errors)

    def test_invalid_state_type(self):
        """Invalid state type returns SYNTAX_ERROR."""
        asl = {
            "StartAt": "Bad",
            "States": {
                "Bad": {"Type": "InvalidType", "End": True}
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("invalid type" in e.lower() for e in result.errors)

    def test_missing_type_field(self):
        """State missing Type field returns SYNTAX_ERROR."""
        asl = {
            "StartAt": "NoType",
            "States": {
                "NoType": {"Resource": "...", "End": True}
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("Type" in e for e in result.errors)

    def test_start_at_references_nonexistent_state(self):
        """StartAt referencing a missing state returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "NonExistent",
            "States": {
                "ActualState": {"Type": "Succeed"}
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("NonExistent" in e for e in result.errors)

    def test_next_references_nonexistent_state(self):
        """Next referencing a missing state returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "First",
            "States": {
                "First": {"Type": "Pass", "Next": "DoesNotExist"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("DoesNotExist" in e for e in result.errors)

    def test_choice_branch_references_nonexistent_state(self):
        """Choice branch targeting a missing state returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.foo",
                            "StringEquals": "bar",
                            "Next": "MissingState",
                        }
                    ],
                    "Default": "FallbackState",
                },
                "FallbackState": {"Type": "Succeed"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("MissingState" in e for e in result.errors)

    def test_choice_default_references_nonexistent_state(self):
        """Choice Default targeting a missing state returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.foo",
                            "StringEquals": "bar",
                            "Next": "BranchState",
                        }
                    ],
                    "Default": "MissingDefault",
                },
                "BranchState": {"Type": "Succeed"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("MissingDefault" in e for e in result.errors)

    def test_valid_choice_state(self):
        """A valid Choice state with proper targets returns SUCCESS."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.type",
                            "StringEquals": "A",
                            "Next": "HandleA",
                        },
                        {
                            "Variable": "$.type",
                            "StringEquals": "B",
                            "Next": "HandleB",
                        },
                    ],
                    "Default": "HandleDefault",
                },
                "HandleA": {"Type": "Succeed"},
                "HandleB": {"Type": "Succeed"},
                "HandleDefault": {"Type": "Fail", "Error": "UnknownType"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS
        assert result.errors == []

    def test_valid_parallel_state(self):
        """A valid Parallel state returns SUCCESS."""
        asl = {
            "StartAt": "ParallelState",
            "States": {
                "ParallelState": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "BranchA",
                            "States": {
                                "BranchA": {"Type": "Pass", "End": True}
                            },
                        },
                        {
                            "StartAt": "BranchB",
                            "States": {
                                "BranchB": {"Type": "Succeed"}
                            },
                        },
                    ],
                    "End": True,
                }
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS

    def test_parallel_branch_invalid_start_at(self):
        """Parallel branch with invalid StartAt returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "ParallelState",
            "States": {
                "ParallelState": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "NonExistentBranch",
                            "States": {
                                "ActualBranch": {"Type": "Pass", "End": True}
                            },
                        }
                    ],
                    "End": True,
                }
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("NonExistentBranch" in e for e in result.errors)

    def test_valid_map_state(self):
        """A valid Map state with ItemProcessor returns SUCCESS."""
        asl = {
            "StartAt": "MapState",
            "States": {
                "MapState": {
                    "Type": "Map",
                    "ItemProcessor": {
                        "StartAt": "ProcessItem",
                        "States": {
                            "ProcessItem": {"Type": "Task", "Resource": "...", "End": True}
                        },
                    },
                    "End": True,
                }
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS

    def test_map_item_processor_invalid_start_at(self):
        """Map ItemProcessor with invalid StartAt returns REFERENCE_ERROR."""
        asl = {
            "StartAt": "MapState",
            "States": {
                "MapState": {
                    "Type": "Map",
                    "ItemProcessor": {
                        "StartAt": "NonExistentProcessor",
                        "States": {
                            "ActualProcessor": {"Type": "Pass", "End": True}
                        },
                    },
                    "End": True,
                }
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.REFERENCE_ERROR
        assert any("NonExistentProcessor" in e for e in result.errors)

    def test_all_valid_state_types(self):
        """All valid state types are accepted without error."""
        for state_type in VALID_STATE_TYPES:
            state_def: dict = {"Type": state_type}
            if state_type not in ("Succeed", "Fail", "Choice"):
                state_def["End"] = True
            if state_type == "Task":
                state_def["Resource"] = "arn:aws:..."
            if state_type == "Choice":
                state_def["Choices"] = [
                    {"Variable": "$.x", "StringEquals": "y", "Next": "End"}
                ]
                state_def["Default"] = "End"

            # Build a machine with this state and an End state
            states = {"TestState": state_def}
            if state_type == "Choice":
                states["End"] = {"Type": "Succeed"}

            asl = {"StartAt": "TestState", "States": states}
            result = validate_asl_definition(asl)

            assert result.category == ValidationCategory.SUCCESS, (
                f"State type '{state_type}' unexpectedly failed: {result.errors}"
            )

    def test_file_path_included_in_result(self):
        """The file_path is included in the result."""
        asl = {
            "StartAt": "S",
            "States": {"S": {"Type": "Succeed"}},
        }
        result = validate_asl_definition(asl, file_path="/my/path.asl.json")

        assert result.file_path == "/my/path.asl.json"

    def test_default_file_path(self):
        """Default file_path is '<unknown>'."""
        asl = {
            "StartAt": "S",
            "States": {"S": {"Type": "Succeed"}},
        }
        result = validate_asl_definition(asl)

        assert result.file_path == "<unknown>"

    def test_syntax_error_takes_priority_over_reference_error(self):
        """When both syntax and reference errors exist, SYNTAX_ERROR is returned."""
        asl = {
            "StartAt": "NonExistent",
            "States": {
                "BadState": {"Type": "NotAValidType", "End": True}
            },
        }
        result = validate_asl_definition(asl)

        # Syntax error (invalid type) takes priority
        assert result.category == ValidationCategory.SYNTAX_ERROR

    def test_state_def_not_a_dict(self):
        """A state definition that is not a dict produces SYNTAX_ERROR."""
        asl = {
            "StartAt": "BadDef",
            "States": {
                "BadDef": "not a dict"
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SYNTAX_ERROR
        assert any("object" in e for e in result.errors)

    def test_wait_state_with_next(self):
        """A Wait state with a valid Next is accepted."""
        asl = {
            "StartAt": "WaitState",
            "States": {
                "WaitState": {"Type": "Wait", "Seconds": 10, "Next": "Done"},
                "Done": {"Type": "Succeed"},
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS

    def test_succeed_state_no_next_required(self):
        """Succeed state doesn't need Next or End."""
        asl = {
            "StartAt": "Done",
            "States": {
                "Done": {"Type": "Succeed"}
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS
        # No warnings about missing Next/End for terminal states
        assert not any("neither" in w.lower() for w in result.warnings)

    def test_fail_state_no_next_required(self):
        """Fail state doesn't need Next or End."""
        asl = {
            "StartAt": "FailState",
            "States": {
                "FailState": {"Type": "Fail", "Error": "SomeError", "Cause": "Reason"}
            },
        }
        result = validate_asl_definition(asl)

        assert result.category == ValidationCategory.SUCCESS
