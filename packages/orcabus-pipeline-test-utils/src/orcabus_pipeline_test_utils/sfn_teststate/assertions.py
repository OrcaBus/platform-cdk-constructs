"""TestState API result assertions.

Provides TestStateAssertion class for verifying TestState API responses:
- Status assertions (SUCCEEDED, FAILED, CAUGHT_ERROR, RETRIABLE)
- Output JSON matching with wildcard support
- Next state verification
- Data flow inspection (afterInputPath, afterParameters, etc.)
- Error handling assertions (catch index, retry backoff)
- Path execution assertions (states visited, terminal state)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from orcabus_pipeline_test_utils.assertions import (
    ANY_STRING_PLACEHOLDER,
    AssertionResult,
    match_json,
)
from orcabus_pipeline_test_utils.sfn_teststate.client import TestStateResult


class TestStateAssertion:
    """Assertion helper for TestState API results.

    Provides methods to verify:
    - State execution status
    - Output JSON structure with wildcard support
    - Next state transitions
    - Input/output data processing at each stage
    - Error handler activation (catch/retry)
    - Execution path traversal
    """

    def __init__(self, result: TestStateResult) -> None:
        """Initialise with a TestState result.

        Args:
            result: The TestStateResult from TestStateClient.test_state().
        """
        self._result = result

    @property
    def result(self) -> TestStateResult:
        """Return the underlying TestStateResult."""
        return self._result

    def assert_status(self, expected_status: str) -> AssertionResult:
        """Assert the state execution reached the expected status.

        Args:
            expected_status: Expected status (SUCCEEDED, FAILED, CAUGHT_ERROR,
                RETRIABLE).

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        if self._result.status != expected_status:
            result.add_error(
                f"Status mismatch: expected={expected_status!r}, "
                f"actual={self._result.status!r}"
            )
        return result

    def assert_succeeded(self) -> AssertionResult:
        """Assert the state execution succeeded."""
        return self.assert_status("SUCCEEDED")

    def assert_failed(self) -> AssertionResult:
        """Assert the state execution failed."""
        return self.assert_status("FAILED")

    def assert_caught_error(self) -> AssertionResult:
        """Assert the error was caught by a Catch handler."""
        return self.assert_status("CAUGHT_ERROR")

    def assert_retriable(self) -> AssertionResult:
        """Assert the error is retriable."""
        return self.assert_status("RETRIABLE")

    def assert_next_state(self, expected_next: str) -> AssertionResult:
        """Assert the next state transition.

        Args:
            expected_next: The expected next state name.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        if self._result.next_state != expected_next:
            result.add_error(
                f"Next state mismatch: expected={expected_next!r}, "
                f"actual={self._result.next_state!r}"
            )
        return result

    def assert_output(self, expected_output: Any) -> AssertionResult:
        """Assert the state output matches the expected structure.

        Supports {% any_string %} wildcard placeholder.

        Args:
            expected_output: The expected output structure.

        Returns:
            AssertionResult indicating pass/fail with mismatch details.
        """
        result = AssertionResult(passed=True)

        if self._result.output is None:
            result.add_error(
                "State has no output (status may be FAILED or RETRIABLE). "
                f"Status: {self._result.status}"
            )
            return result

        errors = match_json(self._result.output, expected_output)
        for error in errors:
            result.add_error(error)

        return result

    def assert_error(
        self,
        expected_error: str | None = None,
        expected_cause: str | None = None,
    ) -> AssertionResult:
        """Assert the error name and/or cause.

        Args:
            expected_error: Expected error name (e.g., "Lambda.ServiceException").
            expected_cause: Expected error cause string.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)

        if expected_error is not None:
            if self._result.error != expected_error:
                result.add_error(
                    f"Error mismatch: expected={expected_error!r}, "
                    f"actual={self._result.error!r}"
                )

        if expected_cause is not None:
            if self._result.cause != expected_cause:
                result.add_error(
                    f"Cause mismatch: expected={expected_cause!r}, "
                    f"actual={self._result.cause!r}"
                )

        return result

    def assert_data_flow(
        self,
        *,
        after_input_path: Any | None = None,
        after_parameters: Any | None = None,
        after_result_selector: Any | None = None,
        after_result_path: Any | None = None,
    ) -> AssertionResult:
        """Assert intermediate data processing results.

        Requires inspection_level=DEBUG. Each parameter is optional;
        only provided values are checked.

        Args:
            after_input_path: Expected value after InputPath is applied.
            after_parameters: Expected value after Parameters/Arguments is applied.
            after_result_selector: Expected value after ResultSelector is applied.
            after_result_path: Expected value after ResultPath is applied.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        inspection = self._result.inspection_data

        if not inspection:
            result.add_error(
                "No inspectionData available. Use inspection_level='DEBUG'."
            )
            return result

        checks = [
            ("afterInputPath", after_input_path),
            ("afterParameters", after_parameters),
            ("afterResultSelector", after_result_selector),
            ("afterResultPath", after_result_path),
        ]

        for field_name, expected in checks:
            if expected is None:
                continue

            raw_value = inspection.get(field_name)
            if raw_value is None:
                result.add_error(
                    f"inspectionData.{field_name} is not present in response"
                )
                continue

            # Parse the raw JSON string
            try:
                actual = json.loads(raw_value)
            except (json.JSONDecodeError, TypeError):
                actual = raw_value

            errors = match_json(actual, expected)
            for error in errors:
                result.add_error(f"inspectionData.{field_name}: {error}")

        return result

    def assert_catch_index(self, expected_index: int) -> AssertionResult:
        """Assert which Catch handler caught the error.

        Args:
            expected_index: The zero-based index of the expected Catch handler.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        inspection = self._result.inspection_data
        error_details = inspection.get("errorDetails", {})
        actual_index = error_details.get("catchIndex")

        if actual_index is None:
            result.add_error(
                "No catchIndex in inspectionData.errorDetails. "
                "State may not have caught the error."
            )
        elif actual_index != expected_index:
            result.add_error(
                f"Catch index mismatch: expected={expected_index}, "
                f"actual={actual_index}"
            )

        return result

    def assert_retry_backoff(
        self,
        expected_seconds: float | None = None,
        expected_retry_index: int | None = None,
    ) -> AssertionResult:
        """Assert retry backoff configuration.

        Args:
            expected_seconds: Expected backoff interval in seconds.
            expected_retry_index: Expected zero-based index of the Retry handler.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        inspection = self._result.inspection_data
        error_details = inspection.get("errorDetails", {})

        if expected_seconds is not None:
            actual = error_details.get("retryBackoffIntervalSeconds")
            if actual is None:
                result.add_error(
                    "No retryBackoffIntervalSeconds in errorDetails."
                )
            elif actual != expected_seconds:
                result.add_error(
                    f"Retry backoff mismatch: expected={expected_seconds}s, "
                    f"actual={actual}s"
                )

        if expected_retry_index is not None:
            actual_idx = error_details.get("retryIndex")
            if actual_idx is None:
                result.add_error("No retryIndex in errorDetails.")
            elif actual_idx != expected_retry_index:
                result.add_error(
                    f"Retry index mismatch: expected={expected_retry_index}, "
                    f"actual={actual_idx}"
                )

        return result


class PathAssertion:
    """Assertion helper for chained TestState path results.

    Provides methods to verify execution paths produced by
    TestStateClient.test_path().
    """

    def __init__(self, results: list[TestStateResult]) -> None:
        """Initialise with a list of path results.

        Args:
            results: Ordered list of TestStateResult from test_path().
        """
        self._results = results

    @property
    def states_visited(self) -> list[str]:
        """Return the list of state transitions from the execution path.

        Note: The TestState API does not echo the state name in its response.
        This property returns the `next_state` values from each result
        (excluding the last), representing the transitions observed during
        the path execution. Use `assert_step_count` for verifying the
        number of states actually executed.
        """
        return [r.next_state for r in self._results[:-1] if r.next_state] if self._results else []

    @property
    def terminal_status(self) -> str:
        """Return the status of the last state in the path."""
        if not self._results:
            return "UNKNOWN"
        return self._results[-1].status

    @property
    def terminal_output(self) -> Any:
        """Return the output of the last state in the path."""
        if not self._results:
            return None
        return self._results[-1].output

    def assert_path_succeeded(self) -> AssertionResult:
        """Assert the entire path completed with the last state succeeding."""
        result = AssertionResult(passed=True)
        if not self._results:
            result.add_error("No results in path.")
            return result

        last = self._results[-1]
        if last.status != "SUCCEEDED":
            result.add_error(
                f"Path did not succeed. Last state status: {last.status}"
            )
        # Terminal state should have no next_state (End state)
        if last.next_state:
            result.add_error(
                f"Path did not reach terminal state. "
                f"Last nextState: {last.next_state!r}"
            )
        return result

    def assert_path_failed(self) -> AssertionResult:
        """Assert the path ended in a failure."""
        result = AssertionResult(passed=True)
        if not self._results:
            result.add_error("No results in path.")
            return result

        last = self._results[-1]
        if last.status not in ("FAILED", "CAUGHT_ERROR"):
            result.add_error(
                f"Path did not fail. Last state status: {last.status}"
            )
        return result

    def assert_step_count(self, expected_count: int) -> AssertionResult:
        """Assert the number of states traversed.

        Args:
            expected_count: Expected number of state executions.

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        actual = len(self._results)
        if actual != expected_count:
            result.add_error(
                f"Step count mismatch: expected={expected_count}, actual={actual}"
            )
        return result

    def assert_terminal_output(self, expected_output: Any) -> AssertionResult:
        """Assert the final output of the path.

        Args:
            expected_output: Expected output structure (supports wildcards).

        Returns:
            AssertionResult indicating pass/fail.
        """
        result = AssertionResult(passed=True)
        if not self._results:
            result.add_error("No results in path.")
            return result

        last = self._results[-1]
        if last.output is None:
            result.add_error("Terminal state has no output.")
            return result

        errors = match_json(last.output, expected_output)
        for error in errors:
            result.add_error(error)

        return result
