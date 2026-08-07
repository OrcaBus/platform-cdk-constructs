"""TestState API client wrapper.

Wraps boto3's stepfunctions.test_state() API for testing individual states
in Step Functions definitions. Supports:
- Testing individual states with mocked service integrations
- Testing states within a full state machine definition (stateName parameter)
- Chaining state executions to simulate execution paths
- DEBUG/TRACE inspection levels for data flow verification
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

import boto3

logger = logging.getLogger(__name__)

_DEFAULT_REGION = "ap-southeast-2"


class TestStateClientError(Exception):
    """Raised when the TestState API returns an error."""


@dataclass
class TestStateResult:
    """Parsed result from a TestState API call.

    Attributes:
        status: The execution status (SUCCEEDED, FAILED, RETRIABLE, CAUGHT_ERROR).
        output: The parsed JSON output from the state (None if failed without output).
        next_state: The next state to transition to (empty string if End state).
        error: The error name if the state failed.
        cause: The error cause if the state failed.
        inspection_data: The raw inspectionData dict (present with DEBUG/TRACE levels).
        raw_response: The full API response dict.
    """

    status: str
    output: Any = None
    next_state: str = ""
    error: str | None = None
    cause: str | None = None
    inspection_data: dict = field(default_factory=dict)
    raw_response: dict = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        """Return True if the state execution succeeded."""
        return self.status == "SUCCEEDED"

    @property
    def failed(self) -> bool:
        """Return True if the state execution failed."""
        return self.status == "FAILED"

    @property
    def caught_error(self) -> bool:
        """Return True if the error was caught by a Catch handler."""
        return self.status == "CAUGHT_ERROR"

    @property
    def retriable(self) -> bool:
        """Return True if the error is retriable."""
        return self.status == "RETRIABLE"


class TestStateClient:
    """Wrapper around the Step Functions TestState API.

    Provides methods for testing individual states with mocked responses,
    testing states within full definitions, and chaining state executions
    to simulate execution paths.
    """

    def __init__(
        self,
        region_name: str = _DEFAULT_REGION,
        role_arn: str | None = None,
        session: boto3.Session | None = None,
    ) -> None:
        """Initialise the TestState client.

        Args:
            region_name: AWS region for the Step Functions service.
            role_arn: Optional IAM role ARN. Not required when using mocks.
            session: Optional boto3 session. Creates a new one if not provided.
        """
        self._region_name = region_name
        self._role_arn = role_arn
        self._session = session or boto3.Session(region_name=region_name)
        self._client = self._session.client(
            "stepfunctions", region_name=region_name
        )

    def test_state(
        self,
        definition: str | dict,
        input_data: str | dict | None = None,
        *,
        state_name: str | None = None,
        mock_result: str | dict | None = None,
        mock_error: dict | None = None,
        inspection_level: str = "DEBUG",
        role_arn: str | None = None,
        context: dict | None = None,
        state_configuration: dict | None = None,
        field_validation_mode: str | None = None,
    ) -> TestStateResult:
        """Test a single state using the TestState API.

        Args:
            definition: The state definition (single state) or full state machine
                definition (when using state_name). Can be a dict or JSON string.
            input_data: The input to the state. Can be a dict or JSON string.
                Defaults to empty object "{}".
            state_name: When definition is a full state machine, specifies which
                state to test. If None, definition is treated as a single state.
            mock_result: The mocked successful result from the service integration.
                Mutually exclusive with mock_error. Can be a dict or JSON string.
            mock_error: The mocked error response. Must contain "error" and "cause"
                keys. Mutually exclusive with mock_result.
            inspection_level: Level of detail in response: "INFO", "DEBUG", or "TRACE".
            role_arn: Override the default role ARN for this call.
            context: Optional Context object values ($$.Execution.Id, etc.).
            state_configuration: Optional state configuration (e.g., retrierRetryCount).
            field_validation_mode: Mock validation mode: "STRICT", "PRESENT", or "NONE".

        Returns:
            TestStateResult with parsed response data.

        Raises:
            TestStateClientError: If the API call fails.
        """
        # Normalise definition to JSON string
        if isinstance(definition, dict):
            definition_str = json.dumps(definition)
        else:
            definition_str = definition

        # Normalise input to JSON string
        if input_data is None:
            input_str = "{}"
        elif isinstance(input_data, dict):
            input_str = json.dumps(input_data)
        else:
            input_str = input_data

        # Build the API kwargs
        kwargs: dict[str, Any] = {
            "definition": definition_str,
            "input": input_str,
            "inspectionLevel": inspection_level,
        }

        # Add state_name if provided (testing within a full definition)
        if state_name is not None:
            kwargs["stateName"] = state_name

        # Add role ARN if available (not required with mocks)
        effective_role = role_arn or self._role_arn
        if effective_role is not None:
            kwargs["roleArn"] = effective_role

        # Build mock parameter
        if mock_result is not None and mock_error is not None:
            raise TestStateClientError(
                "Cannot provide both mock_result and mock_error. "
                "Use one or the other."
            )

        if mock_result is not None:
            mock_obj: dict[str, Any] = {}
            if isinstance(mock_result, dict):
                mock_obj["result"] = json.dumps(mock_result)
            else:
                mock_obj["result"] = mock_result
            if field_validation_mode is not None:
                mock_obj["fieldValidationMode"] = field_validation_mode
            kwargs["mock"] = json.dumps(mock_obj)

        if mock_error is not None:
            mock_obj = {"errorOutput": mock_error}
            if field_validation_mode is not None:
                mock_obj["fieldValidationMode"] = field_validation_mode
            kwargs["mock"] = json.dumps(mock_obj)

        # Add context if provided
        if context is not None:
            kwargs["context"] = json.dumps(context)

        # Add state configuration if provided
        if state_configuration is not None:
            kwargs["stateConfiguration"] = json.dumps(state_configuration)

        # Call the API
        logger.debug(
            "TestState API call: state_name=%s, inspection_level=%s",
            state_name,
            inspection_level,
        )
        try:
            response = self._client.test_state(**kwargs)
        except self._client.exceptions.InvalidDefinition as e:
            raise TestStateClientError(
                f"Invalid state definition: {e}"
            ) from e
        except self._client.exceptions.InvalidExecutionInput as e:
            raise TestStateClientError(
                f"Invalid execution input: {e}"
            ) from e
        except Exception as e:
            raise TestStateClientError(
                f"TestState API call failed: {e}"
            ) from e

        # Parse the response
        return self._parse_response(response)

    def test_path(
        self,
        definition: str | dict,
        input_data: str | dict,
        state_mocks: dict[str, dict],
        *,
        start_state: str | None = None,
        max_steps: int = 50,
        inspection_level: str = "DEBUG",
        role_arn: str | None = None,
    ) -> list[TestStateResult]:
        """Chain TestState calls to simulate an execution path.

        Iterates through states by feeding the output of one state as input
        to the next, using the nextState field to determine the path. Stops
        when a terminal state (End=true, no nextState) is reached or max_steps
        is exceeded.

        Args:
            definition: The full state machine definition (dict or JSON string).
            input_data: The initial input to the first state.
            state_mocks: A dict mapping state names to their mock configuration.
                Each value should have either "result" or "errorOutput" key.
                Example: {"LaunchDragen": {"result": {"job_id": "123"}}}
            start_state: The state to start from. If None, uses StartAt.
            max_steps: Maximum number of states to traverse. Default 50.
            inspection_level: Inspection level for each call.
            role_arn: Override role ARN for all calls.

        Returns:
            Ordered list of TestStateResult for each state visited.

        Raises:
            TestStateClientError: If any state test fails unexpectedly.
        """
        if isinstance(definition, str):
            definition_dict = json.loads(definition)
        else:
            definition_dict = definition

        # Determine starting state
        current_state = start_state or definition_dict.get("StartAt")
        if current_state is None:
            raise TestStateClientError(
                "No start state specified and definition has no StartAt field."
            )

        # Normalise input
        if isinstance(input_data, dict):
            current_input = json.dumps(input_data)
        else:
            current_input = input_data

        results: list[TestStateResult] = []

        for step in range(max_steps):
            # Get mock for current state
            mock_config = state_mocks.get(current_state, {})
            mock_result = mock_config.get("result")
            mock_error = mock_config.get("errorOutput")

            # Build mock kwargs
            mock_kwargs: dict[str, Any] = {}
            if mock_result is not None:
                mock_kwargs["mock_result"] = mock_result
            if mock_error is not None:
                mock_kwargs["mock_error"] = mock_error

            # Execute the state
            result = self.test_state(
                definition=definition_dict,
                input_data=current_input,
                state_name=current_state,
                inspection_level=inspection_level,
                role_arn=role_arn,
                **mock_kwargs,
            )
            results.append(result)

            logger.info(
                "Step %d: state=%s, status=%s, next=%s",
                step + 1,
                current_state,
                result.status,
                result.next_state,
            )

            # Stop on terminal states or errors
            if result.status in ("FAILED", "RETRIABLE"):
                break

            # If caught error, follow the catch handler's next state
            if result.caught_error:
                if result.next_state:
                    current_state = result.next_state
                    current_input = (
                        json.dumps(result.output)
                        if result.output is not None
                        else "{}"
                    )
                    continue
                else:
                    break

            # Check if this is an End state (no next_state)
            if not result.next_state:
                break

            # Move to next state
            current_state = result.next_state
            current_input = (
                json.dumps(result.output)
                if result.output is not None
                else "{}"
            )

        return results

    @staticmethod
    def _parse_response(response: dict) -> TestStateResult:
        """Parse a raw TestState API response into a TestStateResult.

        Args:
            response: The raw boto3 response dict.

        Returns:
            Parsed TestStateResult.
        """
        status = response.get("status", "UNKNOWN")

        # Parse output JSON
        raw_output = response.get("output")
        output = None
        if raw_output is not None:
            try:
                output = json.loads(raw_output)
            except (json.JSONDecodeError, TypeError):
                output = raw_output

        return TestStateResult(
            status=status,
            output=output,
            next_state=response.get("nextState", ""),
            error=response.get("error"),
            cause=response.get("cause"),
            inspection_data=response.get("inspectionData", {}),
            raw_response=response,
        )
