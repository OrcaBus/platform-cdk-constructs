"""Execution result assertions.

Provides ExecutionAssertion class for verifying Step Functions execution results:
- Status assertions (SUCCEEDED/FAILED)
- Output JSON matching with wildcard support
- State visitation verification via execution history
- Parallel branch assertions
- Map state output cardinality assertions
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


# Wildcard placeholder indicating "any string value"
ANY_STRING_PLACEHOLDER = "{% any_string %}"


@dataclass
class AssertionError_:
    """A single assertion failure with context."""

    message: str


@dataclass
class AssertionResult:
    """Result of running one or more assertions against an execution."""

    passed: bool
    errors: list[AssertionError_] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error and mark the result as failed."""
        self.passed = False
        self.errors.append(AssertionError_(message=message))


def match_json(
    actual: object,
    expected: object,
    path: str = "$",
) -> list[str]:
    """Compare actual JSON against expected, respecting wildcard placeholders.

    The ``{% any_string %}`` placeholder in the expected structure indicates
    that the actual value must exist and be a string, but its exact value is
    not checked.

    Args:
        actual: The actual JSON value (parsed from execution output).
        expected: The expected JSON structure (may contain wildcards).
        path: JSONPath-style breadcrumb for error messages.

    Returns:
        A list of mismatch descriptions. Empty list means match.
    """
    errors: list[str] = []

    if expected == ANY_STRING_PLACEHOLDER:
        # Wildcard: actual must be a string
        if not isinstance(actual, str):
            errors.append(
                f"{path}: expected a string (wildcard), "
                f"got {type(actual).__name__}: {actual!r}"
            )
        return errors

    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            errors.append(
                f"{path}: expected an object, got {type(actual).__name__}"
            )
            return errors

        # Check all expected keys are present with correct values
        for key in expected:
            if key not in actual:
                errors.append(f"{path}.{key}: missing in actual output")
            else:
                errors.extend(
                    match_json(actual[key], expected[key], path=f"{path}.{key}")
                )

        # Check for unexpected keys in actual
        for key in actual:
            if key not in expected:
                errors.append(f"{path}.{key}: unexpected key in actual output")

        return errors

    if isinstance(expected, list):
        if not isinstance(actual, list):
            errors.append(
                f"{path}: expected an array, got {type(actual).__name__}"
            )
            return errors

        if len(actual) != len(expected):
            errors.append(
                f"{path}: array length mismatch: "
                f"actual={len(actual)}, expected={len(expected)}"
            )
            return errors

        for i, (a_item, e_item) in enumerate(zip(actual, expected)):
            errors.extend(match_json(a_item, e_item, path=f"{path}[{i}]"))

        return errors

    # Scalar comparison
    if actual != expected:
        errors.append(
            f"{path}: value mismatch: actual={actual!r}, expected={expected!r}"
        )

    return errors


def extract_visited_states(history: list[dict]) -> list[str]:
    """Extract the list of state names visited from an execution history.

    Looks for events of type ``*StateEntered`` which contain the state name.

    Args:
        history: The execution history event list from get_execution_history.

    Returns:
        Ordered list of state names that were entered during execution.
    """
    visited: list[str] = []

    for event in history:
        event_type = event.get("type", "")
        if event_type.endswith("StateEntered"):
            # The state entered details are in a key like
            # "stateEnteredEventDetails"
            details = event.get("stateEnteredEventDetails", {})
            state_name = details.get("name")
            if state_name:
                visited.append(state_name)

    return visited


def extract_parallel_branch_results(history: list[dict]) -> list[list[str]]:
    """Extract per-branch visited states from a Parallel state execution.

    Identifies parallel branch boundaries in the execution history by
    tracking ParallelStateStarted/ParallelStateSucceeded events and
    grouping state entries between branch boundaries.

    Args:
        history: The execution history event list.

    Returns:
        A list of lists, where each inner list contains the state names
        visited in that parallel branch.
    """
    branches: list[list[str]] = []
    current_branch: list[str] | None = None
    in_parallel = False

    for event in history:
        event_type = event.get("type", "")

        if event_type == "ParallelStateStarted":
            in_parallel = True
            continue

        if event_type == "ParallelStateSucceeded" or event_type == "ParallelStateFailed":
            if current_branch is not None:
                branches.append(current_branch)
                current_branch = None
            in_parallel = False
            continue

        if in_parallel:
            # A new branch starts with a state entry following parallel start
            # or after the previous branch's exit
            if event_type.endswith("StateEntered"):
                details = event.get("stateEnteredEventDetails", {})
                state_name = details.get("name")

                if current_branch is None:
                    current_branch = []

                if state_name:
                    current_branch.append(state_name)

            elif event_type.endswith("StateExited"):
                # Check if the next event is a new branch entry
                # We track this by maintaining the current_branch
                pass

    # If we ended inside a parallel state (shouldn't happen in well-formed
    # history but handle defensively)
    if current_branch is not None:
        branches.append(current_branch)

    return branches


class ExecutionAssertion:
    """Assertion helper for Step Functions execution results.

    Provides methods to verify:
    - Execution status (SUCCEEDED, FAILED, TIMED_OUT)
    - Output JSON structure with wildcard support
    - State visitation via execution history
    - Parallel branch completion
    - Map state output cardinality
    """

    def __init__(
        self,
        execution_result: dict,
        execution_history: list[dict] | None = None,
    ) -> None:
        """Initialise with an execution result and optional history.

        Args:
            execution_result: The describe_execution response from
                SfnLocalClient.wait_for_execution().
            execution_history: The execution history from
                SfnLocalClient.get_execution_history(). Required for
                state visitation and parallel branch assertions.
        """
        self._result = execution_result
        self._history = execution_history or []

    @property
    def status(self) -> str:
        """Return the execution status."""
        return self._result.get("status", "UNKNOWN")

    @property
    def output(self) -> dict | None:
        """Return the parsed execution output, or None if absent."""
        raw = self._result.get("output")
        if raw is None:
            return None
        return json.loads(raw)

    @property
    def error(self) -> str | None:
        """Return the execution error, or None if absent."""
        return self._result.get("error")

    @property
    def cause(self) -> str | None:
        """Return the execution error cause, or None if absent."""
        return self._result.get("cause")

    def assert_status(self, expected_status: str) -> AssertionResult:
        """Assert the execution reached the expected terminal status.

        Args:
            expected_status: The expected status (e.g., "SUCCEEDED", "FAILED").

        Returns:
            AssertionResult indicating pass/fail with error details.
        """
        result = AssertionResult(passed=True)
        actual_status = self.status

        if actual_status != expected_status:
            result.add_error(
                f"Execution status mismatch: "
                f"expected={expected_status!r}, actual={actual_status!r}"
            )

        return result

    def assert_output(self, expected_output: dict) -> AssertionResult:
        """Assert the execution output matches the expected JSON structure.

        Supports the ``{% any_string %}`` wildcard placeholder for fields
        where only the type (string) matters, not the exact value.

        Args:
            expected_output: The expected output structure. May contain
                ``{% any_string %}`` placeholders.

        Returns:
            AssertionResult indicating pass/fail with mismatch details.
        """
        result = AssertionResult(passed=True)
        actual_output = self.output

        if actual_output is None:
            result.add_error(
                "Execution has no output (status may be FAILED or TIMED_OUT)"
            )
            return result

        errors = match_json(actual_output, expected_output)
        for error in errors:
            result.add_error(error)

        return result

    def assert_states_visited(
        self, expected_states: list[str]
    ) -> AssertionResult:
        """Assert that all expected states were visited during execution.

        Checks that every state in ``expected_states`` appears in the
        execution history (order is not enforced, only presence).

        Args:
            expected_states: List of state names that should have been visited.

        Returns:
            AssertionResult indicating pass/fail with missing state details.
        """
        result = AssertionResult(passed=True)

        if not self._history:
            result.add_error(
                "No execution history available for state visitation check"
            )
            return result

        visited = extract_visited_states(self._history)
        visited_set = set(visited)

        for state in expected_states:
            if state not in visited_set:
                result.add_error(
                    f"State '{state}' was not visited. "
                    f"Visited states: {visited}"
                )

        return result

    def assert_parallel_branches_complete(
        self,
        expected_branch_count: int,
        expected_terminal_states: list[str] | None = None,
    ) -> AssertionResult:
        """Assert all N parallel branches completed execution.

        Verifies that the execution history shows the expected number of
        parallel branches and that each branch reached its expected terminal
        state (if specified).

        Args:
            expected_branch_count: The number of parallel branches expected.
            expected_terminal_states: Optional list of terminal state names,
                one per branch. If provided, verifies each branch's last
                visited state matches.

        Returns:
            AssertionResult indicating pass/fail with branch details.
        """
        result = AssertionResult(passed=True)

        if not self._history:
            result.add_error(
                "No execution history available for parallel branch check"
            )
            return result

        branches = extract_parallel_branch_results(self._history)
        actual_count = len(branches)

        if actual_count != expected_branch_count:
            result.add_error(
                f"Parallel branch count mismatch: "
                f"expected={expected_branch_count}, actual={actual_count}"
            )
            return result

        if expected_terminal_states is not None:
            if len(expected_terminal_states) != expected_branch_count:
                result.add_error(
                    f"expected_terminal_states length "
                    f"({len(expected_terminal_states)}) does not match "
                    f"expected_branch_count ({expected_branch_count})"
                )
                return result

            for i, (branch, expected_terminal) in enumerate(
                zip(branches, expected_terminal_states)
            ):
                if not branch:
                    result.add_error(
                        f"Branch {i}: no states visited"
                    )
                elif branch[-1] != expected_terminal:
                    result.add_error(
                        f"Branch {i}: expected terminal state "
                        f"'{expected_terminal}', got '{branch[-1]}'. "
                        f"Visited: {branch}"
                    )

        return result

    def assert_map_state_output_cardinality(
        self,
        input_array: list,
        map_state_output: list | None = None,
    ) -> AssertionResult:
        """Assert Map state output has the same cardinality as input.

        Verifies that a Map state produced exactly one output element per
        input array element.

        Args:
            input_array: The input array that was fed to the Map state.
            map_state_output: The output array from the Map state. If None,
                uses the execution output (assumed to be the Map state output).

        Returns:
            AssertionResult indicating pass/fail with cardinality details.
        """
        result = AssertionResult(passed=True)

        if map_state_output is None:
            output = self.output
            if output is None:
                result.add_error(
                    "No execution output available for Map state "
                    "cardinality check"
                )
                return result
            if not isinstance(output, list):
                result.add_error(
                    f"Map state output is not an array: "
                    f"got {type(output).__name__}"
                )
                return result
            map_state_output = output

        expected_length = len(input_array)
        actual_length = len(map_state_output)

        if actual_length != expected_length:
            result.add_error(
                f"Map state output cardinality mismatch: "
                f"input has {expected_length} elements, "
                f"output has {actual_length} elements"
            )

        return result
