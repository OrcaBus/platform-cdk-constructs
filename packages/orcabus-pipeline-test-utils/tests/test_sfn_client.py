"""Unit tests for SfnLocalClient boto3 wrapper."""

from __future__ import annotations

import json
import time
from unittest.mock import MagicMock, patch

import pytest

from orcabus_pipeline_test_utils.sfn_local.client import (
    SfnLocalClient,
    SfnLocalClientError,
    _DEFAULT_ENDPOINT,
    _DEFAULT_ROLE_ARN,
    _POLL_INTERVAL,
    _TERMINAL_STATUSES,
)


@pytest.fixture
def mock_boto3_client() -> MagicMock:
    """Create a mock boto3 stepfunctions client."""
    return MagicMock()


@pytest.fixture
def sfn_client(mock_boto3_client: MagicMock) -> SfnLocalClient:
    """Create an SfnLocalClient with a mocked boto3 client."""
    with patch("orcabus_pipeline_test_utils.sfn_local.client.boto3.client") as mock_ctor:
        mock_ctor.return_value = mock_boto3_client
        client = SfnLocalClient()
    return client


@pytest.fixture
def sfn_client_custom_endpoint(mock_boto3_client: MagicMock) -> SfnLocalClient:
    """Create an SfnLocalClient with a custom endpoint."""
    with patch("orcabus_pipeline_test_utils.sfn_local.client.boto3.client") as mock_ctor:
        mock_ctor.return_value = mock_boto3_client
        client = SfnLocalClient(endpoint_url="http://localhost:9999")
    return client


class TestSfnLocalClientInit:
    """Test SfnLocalClient initialization."""

    def test_default_endpoint(self, sfn_client: SfnLocalClient) -> None:
        assert sfn_client.endpoint_url == _DEFAULT_ENDPOINT

    def test_custom_endpoint(
        self, sfn_client_custom_endpoint: SfnLocalClient
    ) -> None:
        assert sfn_client_custom_endpoint.endpoint_url == "http://localhost:9999"

    def test_boto3_client_configured_correctly(self) -> None:
        with patch("orcabus_pipeline_test_utils.sfn_local.client.boto3.client") as mock_ctor:
            mock_ctor.return_value = MagicMock()
            SfnLocalClient(endpoint_url="http://localhost:8083")

        mock_ctor.assert_called_once_with(
            "stepfunctions",
            endpoint_url="http://localhost:8083",
            region_name="ap-southeast-2",
            aws_access_key_id="testing",
            aws_secret_access_key="testing",  # pragma: allowlist secret
        )


class TestCreateStateMachine:
    """Test SfnLocalClient.create_state_machine()."""

    def test_create_state_machine_returns_arn(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        expected_arn = "arn:aws:states:ap-southeast-2:123456789012:stateMachine:test-sm"
        mock_boto3_client.create_state_machine.return_value = {
            "stateMachineArn": expected_arn,
            "creationDate": "2024-01-01T00:00:00Z",
        }

        definition = {
            "StartAt": "Start",
            "States": {"Start": {"Type": "Pass", "End": True}},
        }
        arn = sfn_client.create_state_machine("test-sm", definition)

        assert arn == expected_arn
        mock_boto3_client.create_state_machine.assert_called_once_with(
            name="test-sm",
            definition=json.dumps(definition),
            roleArn=_DEFAULT_ROLE_ARN,
        )

    def test_create_state_machine_custom_role_arn(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        custom_role = "arn:aws:iam::999999999999:role/custom"
        mock_boto3_client.create_state_machine.return_value = {
            "stateMachineArn": "arn:aws:states:ap-southeast-2:123456789012:stateMachine:sm",
        }

        definition = {"StartAt": "S", "States": {"S": {"Type": "Pass", "End": True}}}
        sfn_client.create_state_machine("sm", definition, role_arn=custom_role)

        call_kwargs = mock_boto3_client.create_state_machine.call_args[1]
        assert call_kwargs["roleArn"] == custom_role

    def test_create_state_machine_raises_on_error(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        mock_boto3_client.create_state_machine.side_effect = Exception("InvalidASL")

        with pytest.raises(SfnLocalClientError, match="Failed to create state machine"):
            sfn_client.create_state_machine("bad-sm", {"invalid": True})

    def test_create_state_machine_serializes_definition_to_json(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        mock_boto3_client.create_state_machine.return_value = {
            "stateMachineArn": "arn:aws:states:ap-southeast-2:123456789012:stateMachine:sm",
        }
        definition = {
            "StartAt": "Task1",
            "States": {
                "Task1": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:fn",
                    "End": True,
                },
            },
        }
        sfn_client.create_state_machine("sm", definition)

        call_kwargs = mock_boto3_client.create_state_machine.call_args[1]
        # Verify it's valid JSON
        parsed = json.loads(call_kwargs["definition"])
        assert parsed == definition


class TestStartExecution:
    """Test SfnLocalClient.start_execution()."""

    def test_start_execution_returns_execution_arn(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        expected_arn = (
            "arn:aws:states:ap-southeast-2:123456789012:execution:test-sm:HappyPath"
        )
        mock_boto3_client.start_execution.return_value = {
            "executionArn": expected_arn,
            "startDate": "2024-01-01T00:00:00Z",
        }

        sm_arn = "arn:aws:states:ap-southeast-2:123456789012:stateMachine:test-sm"
        execution_arn = sfn_client.start_execution(
            sm_arn, "HappyPath", {"key": "value"}
        )

        assert execution_arn == expected_arn

    def test_start_execution_appends_test_case_suffix(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        mock_boto3_client.start_execution.return_value = {
            "executionArn": "arn:aws:states:ap-southeast-2:123456789012:execution:sm:TestCase",
        }

        sm_arn = "arn:aws:states:ap-southeast-2:123456789012:stateMachine:sm"
        sfn_client.start_execution(sm_arn, "TestCase", {})

        call_kwargs = mock_boto3_client.start_execution.call_args[1]
        assert call_kwargs["stateMachineArn"] == f"{sm_arn}#TestCase"
        assert call_kwargs["name"] == "TestCase"

    def test_start_execution_serializes_input_to_json(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        mock_boto3_client.start_execution.return_value = {
            "executionArn": "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1",
        }

        input_data = {"workflow_name": "dragen-wgts-dna", "sample_id": "SMP001"}
        sm_arn = "arn:aws:states:ap-southeast-2:123456789012:stateMachine:sm"
        sfn_client.start_execution(sm_arn, "T1", input_data)

        call_kwargs = mock_boto3_client.start_execution.call_args[1]
        assert json.loads(call_kwargs["input"]) == input_data

    def test_start_execution_raises_on_error(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        mock_boto3_client.start_execution.side_effect = Exception("SM not found")

        with pytest.raises(SfnLocalClientError, match="Failed to start execution"):
            sfn_client.start_execution("arn:invalid", "TestCase", {})


class TestWaitForExecution:
    """Test SfnLocalClient.wait_for_execution()."""

    def test_wait_returns_on_succeeded(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "SUCCEEDED",
            "output": '{"result": "ok"}',
        }

        result = sfn_client.wait_for_execution(execution_arn)

        assert result["status"] == "SUCCEEDED"
        assert result["output"] == '{"result": "ok"}'

    def test_wait_returns_on_failed(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "FAILED",
            "error": "States.TaskFailed",
            "cause": "Lambda threw an error",
        }

        result = sfn_client.wait_for_execution(execution_arn)

        assert result["status"] == "FAILED"

    def test_wait_returns_on_timed_out(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "TIMED_OUT",
        }

        result = sfn_client.wait_for_execution(execution_arn)

        assert result["status"] == "TIMED_OUT"

    def test_wait_returns_on_aborted(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "ABORTED",
        }

        result = sfn_client.wait_for_execution(execution_arn)

        assert result["status"] == "ABORTED"

    def test_wait_polls_until_terminal_status(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        # First two calls return RUNNING, third returns SUCCEEDED
        mock_boto3_client.describe_execution.side_effect = [
            {"executionArn": execution_arn, "status": "RUNNING"},
            {"executionArn": execution_arn, "status": "RUNNING"},
            {"executionArn": execution_arn, "status": "SUCCEEDED", "output": "{}"},
        ]

        with patch("orcabus_pipeline_test_utils.sfn_local.client.time.sleep"):
            result = sfn_client.wait_for_execution(execution_arn)

        assert result["status"] == "SUCCEEDED"
        assert mock_boto3_client.describe_execution.call_count == 3

    def test_wait_raises_on_timeout(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "RUNNING",
        }

        with patch(
            "orcabus_pipeline_test_utils.sfn_local.client.time.monotonic"
        ) as mock_monotonic:
            # Simulate time passing beyond the timeout
            mock_monotonic.side_effect = [0.0, 0.0, 31.0]
            with pytest.raises(SfnLocalClientError, match="did not complete within"):
                sfn_client.wait_for_execution(execution_arn, timeout=30)

    def test_wait_raises_on_describe_error(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.side_effect = Exception("Connection lost")

        with pytest.raises(SfnLocalClientError, match="Failed to describe execution"):
            sfn_client.wait_for_execution(execution_arn)

    def test_wait_uses_custom_timeout(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.describe_execution.return_value = {
            "executionArn": execution_arn,
            "status": "RUNNING",
        }

        with patch(
            "orcabus_pipeline_test_utils.sfn_local.client.time.monotonic"
        ) as mock_monotonic:
            # Simulate time passing beyond the custom 5s timeout
            mock_monotonic.side_effect = [0.0, 0.0, 6.0]
            with pytest.raises(SfnLocalClientError, match="did not complete within 5s"):
                sfn_client.wait_for_execution(execution_arn, timeout=5)


class TestGetExecutionHistory:
    """Test SfnLocalClient.get_execution_history()."""

    def test_get_history_returns_events(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        expected_events = [
            {"timestamp": "2024-01-01T00:00:00Z", "type": "ExecutionStarted", "id": 1},
            {"timestamp": "2024-01-01T00:00:01Z", "type": "TaskStateEntered", "id": 2},
            {"timestamp": "2024-01-01T00:00:02Z", "type": "ExecutionSucceeded", "id": 3},
        ]
        mock_boto3_client.get_execution_history.return_value = {
            "events": expected_events,
        }

        result = sfn_client.get_execution_history(execution_arn)

        assert result == expected_events
        mock_boto3_client.get_execution_history.assert_called_once_with(
            executionArn=execution_arn, maxResults=1000
        )

    def test_get_history_paginates(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        page1_events = [
            {"type": "ExecutionStarted", "id": 1},
            {"type": "TaskStateEntered", "id": 2},
        ]
        page2_events = [
            {"type": "ExecutionSucceeded", "id": 3},
        ]
        mock_boto3_client.get_execution_history.side_effect = [
            {"events": page1_events, "nextToken": "token123"},
            {"events": page2_events},
        ]

        result = sfn_client.get_execution_history(execution_arn)

        assert result == page1_events + page2_events
        assert mock_boto3_client.get_execution_history.call_count == 2

        # Second call should include the nextToken
        second_call_kwargs = mock_boto3_client.get_execution_history.call_args_list[1][1]
        assert second_call_kwargs["nextToken"] == "token123"

    def test_get_history_returns_empty_list_for_no_events(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.get_execution_history.return_value = {"events": []}

        result = sfn_client.get_execution_history(execution_arn)

        assert result == []

    def test_get_history_raises_on_error(
        self, sfn_client: SfnLocalClient, mock_boto3_client: MagicMock
    ) -> None:
        execution_arn = "arn:aws:states:ap-southeast-2:123456789012:execution:sm:T1"
        mock_boto3_client.get_execution_history.side_effect = Exception("Not found")

        with pytest.raises(SfnLocalClientError, match="Failed to get execution history"):
            sfn_client.get_execution_history(execution_arn)
