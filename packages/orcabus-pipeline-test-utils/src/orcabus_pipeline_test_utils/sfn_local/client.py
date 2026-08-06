"""SFN Local client wrapper.

Wraps boto3 client targeting http://localhost:8083 with methods for:
- create_state_machine
- start_execution (with #test_case suffix)
- wait_for_execution (polling until completion)
- get_execution_history
"""

from __future__ import annotations

import json
import logging
import time

import boto3

logger = logging.getLogger(__name__)

_DEFAULT_ENDPOINT = "http://localhost:8083"
_DEFAULT_ROLE_ARN = "arn:aws:iam::123456789012:role/test"
_DEFAULT_TIMEOUT = 30
_POLL_INTERVAL = 0.5  # seconds
_TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"}


class SfnLocalClientError(Exception):
    """Raised when the SFN Local client encounters an error."""


class SfnLocalClient:
    """Boto3 client wrapper targeting Step Functions Local."""

    def __init__(self, endpoint_url: str = _DEFAULT_ENDPOINT) -> None:
        """Initialise the SFN Local client.

        Args:
            endpoint_url: The endpoint URL for the Step Functions Local service.
                Defaults to http://localhost:8083.
        """
        self._endpoint_url = endpoint_url
        self._client = boto3.client(
            "stepfunctions",
            endpoint_url=endpoint_url,
            region_name="ap-southeast-2",
            aws_access_key_id="testing",
            aws_secret_access_key="testing",  # pragma: allowlist secret
        )

    @property
    def endpoint_url(self) -> str:
        """Return the configured endpoint URL."""
        return self._endpoint_url

    def create_state_machine(
        self,
        name: str,
        definition: dict,
        role_arn: str = _DEFAULT_ROLE_ARN,
    ) -> str:
        """Create a state machine and return its ARN.

        Args:
            name: The name for the state machine.
            definition: The ASL definition as a dictionary.
            role_arn: The IAM role ARN for the state machine. Defaults to a
                dummy test ARN.

        Returns:
            The ARN of the created state machine.

        Raises:
            SfnLocalClientError: If the state machine creation fails.
        """
        try:
            response = self._client.create_state_machine(
                name=name,
                definition=json.dumps(definition),
                roleArn=role_arn,
            )
            arn = response["stateMachineArn"]
            logger.info("Created state machine: %s (ARN: %s)", name, arn)
            return arn
        except Exception as e:
            raise SfnLocalClientError(
                f"Failed to create state machine '{name}': {e}"
            ) from e

    def start_execution(
        self,
        state_machine_arn: str,
        test_case: str,
        input_data: dict,
    ) -> str:
        """Start a state machine execution with a #test_case suffix.

        The execution name is constructed as `{test_case}` and the
        state machine ARN is appended with `#{test_case}` to trigger the
        corresponding mock configuration in Step Functions Local.

        Args:
            state_machine_arn: The ARN of the state machine to execute.
            test_case: The test case name (used as #suffix for mock config lookup).
            input_data: The execution input as a dictionary.

        Returns:
            The ARN of the started execution.

        Raises:
            SfnLocalClientError: If starting the execution fails.
        """
        # Step Functions Local uses the #TestCase suffix on the ARN
        # to select the appropriate mock configuration
        suffixed_arn = f"{state_machine_arn}#{test_case}"

        try:
            response = self._client.start_execution(
                stateMachineArn=suffixed_arn,
                name=test_case,
                input=json.dumps(input_data),
            )
            execution_arn = response["executionArn"]
            logger.info(
                "Started execution for test case '%s': %s",
                test_case,
                execution_arn,
            )
            return execution_arn
        except Exception as e:
            raise SfnLocalClientError(
                f"Failed to start execution for test case '{test_case}': {e}"
            ) from e

    def wait_for_execution(
        self,
        execution_arn: str,
        timeout: int = _DEFAULT_TIMEOUT,
    ) -> dict:
        """Poll until execution completes and return the describe-execution result.

        Polls the execution status at regular intervals until it reaches a
        terminal state (SUCCEEDED, FAILED, TIMED_OUT, ABORTED) or the timeout
        is exceeded.

        Args:
            execution_arn: The ARN of the execution to monitor.
            timeout: Maximum seconds to wait for completion. Defaults to 30.

        Returns:
            The full describe_execution response dict.

        Raises:
            SfnLocalClientError: If polling fails or the timeout is exceeded.
        """
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            try:
                response = self._client.describe_execution(
                    executionArn=execution_arn
                )
            except Exception as e:
                raise SfnLocalClientError(
                    f"Failed to describe execution '{execution_arn}': {e}"
                ) from e

            status = response.get("status")
            if status in _TERMINAL_STATUSES:
                logger.info(
                    "Execution %s completed with status: %s",
                    execution_arn,
                    status,
                )
                return response

            time.sleep(_POLL_INTERVAL)

        raise SfnLocalClientError(
            f"Execution '{execution_arn}' did not complete within {timeout}s. "
            f"Last status: {status}"
        )

    def get_execution_history(self, execution_arn: str) -> list[dict]:
        """Return the full execution event history.

        Paginates through all history events for the given execution.

        Args:
            execution_arn: The ARN of the execution to get history for.

        Returns:
            A list of execution history event dicts.

        Raises:
            SfnLocalClientError: If retrieving the history fails.
        """
        events: list[dict] = []
        next_token: str | None = None

        try:
            while True:
                kwargs: dict = {
                    "executionArn": execution_arn,
                    "maxResults": 1000,
                }
                if next_token is not None:
                    kwargs["nextToken"] = next_token

                response = self._client.get_execution_history(**kwargs)
                events.extend(response.get("events", []))

                next_token = response.get("nextToken")
                if not next_token:
                    break
        except Exception as e:
            raise SfnLocalClientError(
                f"Failed to get execution history for '{execution_arn}': {e}"
            ) from e

        logger.info(
            "Retrieved %d history events for execution %s",
            len(events),
            execution_arn,
        )
        return events
