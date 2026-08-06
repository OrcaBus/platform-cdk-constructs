"""Unit tests for the state reference checker module."""

from orcabus_pipeline_test_utils.asl_validation.reference_checker import (
    check_state_references,
)


class TestCheckStateReferences:
    """Tests for the check_state_references function."""

    def test_valid_linear_workflow(self):
        """A linear workflow with valid Next references should produce no errors."""
        asl = {
            "StartAt": "Step1",
            "States": {
                "Step1": {"Type": "Task", "Next": "Step2"},
                "Step2": {"Type": "Task", "Next": "Step3"},
                "Step3": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_dangling_next_reference(self):
        """A 'Next' field referencing a non-existent state should produce an error."""
        asl = {
            "StartAt": "Step1",
            "States": {
                "Step1": {"Type": "Task", "Next": "NonExistent"},
                "Step2": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "NonExistent" in errors[0]
        assert "Step1" in errors[0]

    def test_dangling_start_at(self):
        """A 'StartAt' field referencing a non-existent state should produce an error."""
        asl = {
            "StartAt": "MissingState",
            "States": {
                "Step1": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "MissingState" in errors[0]
        assert "StartAt" in errors[0]

    def test_valid_choice_state(self):
        """A Choice state with valid branch targets and Default should produce no errors."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {"Variable": "$.x", "NumericEquals": 1, "Next": "BranchA"},
                        {"Variable": "$.x", "NumericEquals": 2, "Next": "BranchB"},
                    ],
                    "Default": "FallbackState",
                },
                "BranchA": {"Type": "Succeed"},
                "BranchB": {"Type": "Succeed"},
                "FallbackState": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_dangling_choice_branch_target(self):
        """A Choice rule with a non-existent Next target should produce an error."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {"Variable": "$.x", "NumericEquals": 1, "Next": "MissingBranch"},
                    ],
                    "Default": "FallbackState",
                },
                "FallbackState": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "MissingBranch" in errors[0]
        assert "Choice rule [0]" in errors[0]

    def test_dangling_default_reference(self):
        """A 'Default' field referencing a non-existent state should produce an error."""
        asl = {
            "StartAt": "ChoiceState",
            "States": {
                "ChoiceState": {
                    "Type": "Choice",
                    "Choices": [
                        {"Variable": "$.x", "NumericEquals": 1, "Next": "Step1"},
                    ],
                    "Default": "NonExistentDefault",
                },
                "Step1": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "NonExistentDefault" in errors[0]
        assert "Default" in errors[0]

    def test_valid_catch_references(self):
        """Catch blocks with valid Next targets should produce no errors."""
        asl = {
            "StartAt": "TaskState",
            "States": {
                "TaskState": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123:function:fn",
                    "Next": "SuccessState",
                    "Catch": [
                        {"ErrorEquals": ["States.ALL"], "Next": "ErrorState"},
                    ],
                },
                "SuccessState": {"Type": "Succeed"},
                "ErrorState": {"Type": "Fail"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_dangling_catch_reference(self):
        """A Catch block with a non-existent Next target should produce an error."""
        asl = {
            "StartAt": "TaskState",
            "States": {
                "TaskState": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123:function:fn",
                    "Next": "SuccessState",
                    "Catch": [
                        {"ErrorEquals": ["States.ALL"], "Next": "MissingError"},
                    ],
                },
                "SuccessState": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "MissingError" in errors[0]
        assert "Catch [0]" in errors[0]

    def test_parallel_state_with_valid_branches(self):
        """A Parallel state with internally-valid branches should produce no errors."""
        asl = {
            "StartAt": "ParallelState",
            "States": {
                "ParallelState": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "BranchStep1",
                            "States": {
                                "BranchStep1": {"Type": "Task", "Next": "BranchStep2"},
                                "BranchStep2": {"Type": "Succeed"},
                            },
                        },
                    ],
                    "Next": "Done",
                },
                "Done": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_parallel_state_with_dangling_branch_reference(self):
        """A Parallel branch with an invalid internal reference should produce an error."""
        asl = {
            "StartAt": "ParallelState",
            "States": {
                "ParallelState": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "BranchStep1",
                            "States": {
                                "BranchStep1": {"Type": "Task", "Next": "Missing"},
                            },
                        },
                    ],
                    "Next": "Done",
                },
                "Done": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "Missing" in errors[0]

    def test_parallel_branch_dangling_start_at(self):
        """A Parallel branch with an invalid StartAt should produce an error."""
        asl = {
            "StartAt": "ParallelState",
            "States": {
                "ParallelState": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "NoSuchState",
                            "States": {
                                "BranchStep1": {"Type": "Succeed"},
                            },
                        },
                    ],
                    "Next": "Done",
                },
                "Done": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "NoSuchState" in errors[0]
        assert "StartAt" in errors[0]

    def test_map_state_with_valid_iterator(self):
        """A Map state with a valid Iterator should produce no errors."""
        asl = {
            "StartAt": "MapState",
            "States": {
                "MapState": {
                    "Type": "Map",
                    "Iterator": {
                        "StartAt": "MapStep1",
                        "States": {
                            "MapStep1": {"Type": "Task", "Next": "MapStep2"},
                            "MapStep2": {"Type": "Succeed"},
                        },
                    },
                    "Next": "Done",
                },
                "Done": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_map_state_with_item_processor(self):
        """A Map state using ItemProcessor (newer ASL) should be validated."""
        asl = {
            "StartAt": "MapState",
            "States": {
                "MapState": {
                    "Type": "Map",
                    "ItemProcessor": {
                        "StartAt": "ProcessItem",
                        "States": {
                            "ProcessItem": {"Type": "Task", "Next": "GhostState"},
                        },
                    },
                    "Next": "Done",
                },
                "Done": {"Type": "Succeed"},
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "GhostState" in errors[0]

    def test_multiple_errors_reported(self):
        """Multiple dangling references should all be reported."""
        asl = {
            "StartAt": "Step1",
            "States": {
                "Step1": {"Type": "Task", "Next": "Missing1"},
                "Step2": {
                    "Type": "Choice",
                    "Choices": [
                        {"Variable": "$.x", "NumericEquals": 1, "Next": "Missing2"},
                    ],
                    "Default": "Missing3",
                },
            },
        }
        errors = check_state_references(asl)
        assert len(errors) == 3
        dangling_names = " ".join(errors)
        assert "Missing1" in dangling_names
        assert "Missing2" in dangling_names
        assert "Missing3" in dangling_names

    def test_empty_states_map(self):
        """An ASL with an empty States map and dangling StartAt should produce an error."""
        asl = {
            "StartAt": "Something",
            "States": {},
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "StartAt" in errors[0]

    def test_no_states_key(self):
        """An ASL without a 'States' key should not crash (returns error about States)."""
        asl = {"StartAt": "Something"}
        errors = check_state_references(asl)
        # Should not crash — States defaults to empty dict
        # StartAt will be dangling
        assert len(errors) == 1
        assert "StartAt" in errors[0]

    def test_terminal_states_without_next(self):
        """Succeed and Fail states without Next should not produce errors."""
        asl = {
            "StartAt": "Step1",
            "States": {
                "Step1": {"Type": "Task", "Next": "EndSuccess"},
                "EndSuccess": {"Type": "Succeed"},
                "EndFail": {"Type": "Fail", "Error": "Oops", "Cause": "Something"},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_end_true_without_next(self):
        """A state with 'End': true and no 'Next' should not produce errors."""
        asl = {
            "StartAt": "Step1",
            "States": {
                "Step1": {"Type": "Task", "End": True},
            },
        }
        errors = check_state_references(asl)
        assert errors == []

    def test_states_field_not_dict(self):
        """If 'States' is not a dict, should return an error."""
        asl = {
            "StartAt": "Step1",
            "States": "invalid",
        }
        errors = check_state_references(asl)
        assert len(errors) == 1
        assert "not a valid object" in errors[0]
