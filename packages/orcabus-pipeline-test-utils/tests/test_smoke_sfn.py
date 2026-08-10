"""Unit tests for smoke/sfn_check.py — State Machine checker."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from orcabus_pipeline_test_utils.smoke import SmokeTestResult
from orcabus_pipeline_test_utils.smoke.sfn_check import check_state_machine_active


_SM_ARN = "arn:aws:states:ap-southeast-2:123456789012:stateMachine:my-pipeline-sfn"


@pytest.fixture
def mock_session() -> MagicMock:
    """Create a mock boto3 Session."""
    return MagicMock()


@pytest.fixture
def mock_sfn_client(mock_session: MagicMock) -> MagicMock:
    """Create a mock stepfunctions client wired to the session."""
    client = MagicMock()
    mock_session.client.return_value = client
    return client


class TestCheckStateMachineActiveSuccess:
    """Tests for the happy path — ACTIVE state machine with definition."""

    def test_returns_passed_when_active_with_definition(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "stateMachineArn": _SM_ARN,
            "status": "ACTIVE",
            "definition": '{"StartAt": "Start", "States": {"Start": {"Type": "Pass", "End": true}}}',
            "name": "my-pipeline-sfn",
        }

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is True
        assert result.resource_name == _SM_ARN
        assert result.resource_type == "state_machine"
        assert result.error_type is None
        assert result.error_message is None

    def test_calls_describe_state_machine_with_correct_arn(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "status": "ACTIVE",
            "definition": "{}",
        }

        check_state_machine_active(_SM_ARN, mock_session)

        mock_session.client.assert_called_once_with("stepfunctions")
        mock_sfn_client.describe_state_machine.assert_called_once_with(
            stateMachineArn=_SM_ARN
        )


class TestCheckStateMachineActiveStatusFailures:
    """Tests for non-ACTIVE status conditions."""

    def test_fails_when_status_is_deleting(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "status": "DELETING",
            "definition": '{"StartAt": "X", "States": {}}',
        }

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "DELETING" in result.error_message
        assert "ACTIVE" in result.error_message

    def test_fails_when_definition_is_none(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "status": "ACTIVE",
            "definition": None,
        }

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "null or empty" in result.error_message

    def test_fails_when_definition_is_empty_string(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "status": "ACTIVE",
            "definition": "",
        }

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "null or empty" in result.error_message


class TestCheckStateMachineActiveAuthErrors:
    """Tests for authentication/authorization errors."""

    def test_access_denied_returns_auth_error(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "AccessDeniedException",
                    "Message": "User is not authorized to perform this action",
                }
            },
            operation_name="DescribeStateMachine",
        )

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert "AccessDeniedException" in result.error_message

    def test_expired_token_returns_auth_error(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "ExpiredTokenException",
                    "Message": "The security token has expired",
                }
            },
            operation_name="DescribeStateMachine",
        )

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert "ExpiredTokenException" in result.error_message


class TestCheckStateMachineActiveConfigErrors:
    """Tests for non-auth ClientErrors and generic exceptions."""

    def test_resource_not_found_returns_config_error(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "StateMachineDoesNotExist",
                    "Message": "State machine does not exist",
                }
            },
            operation_name="DescribeStateMachine",
        )

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "StateMachineDoesNotExist" in result.error_message

    def test_generic_exception_returns_config_error(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.side_effect = RuntimeError(
            "Connection timeout"
        )

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "Connection timeout" in result.error_message

    def test_result_is_smoke_test_result_dataclass(
        self, mock_session: MagicMock, mock_sfn_client: MagicMock
    ) -> None:
        mock_sfn_client.describe_state_machine.return_value = {
            "status": "ACTIVE",
            "definition": '{"StartAt": "S", "States": {}}',
        }

        result = check_state_machine_active(_SM_ARN, mock_session)

        assert isinstance(result, SmokeTestResult)
