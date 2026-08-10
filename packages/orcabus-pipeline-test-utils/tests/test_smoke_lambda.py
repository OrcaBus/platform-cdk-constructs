"""Unit tests for the Lambda DryRun smoke check."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import boto3
from botocore.stub import Stubber

from orcabus_pipeline_test_utils.smoke import SmokeTestResult
from orcabus_pipeline_test_utils.smoke.lambda_check import check_lambda_invocable


class TestCheckLambdaInvocable:
    """Tests for check_lambda_invocable function."""

    def test_returns_passed_on_http_204(self) -> None:
        """DryRun returning HTTP 204 should produce passed=True."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_response(
                "invoke",
                {"StatusCode": 204},
                expected_params={
                    "FunctionName": "my-function",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("my-function", session)

        assert result == SmokeTestResult(
            resource_name="my-function",
            resource_type="lambda",
            passed=True,
            error_type=None,
            error_message=None,
        )

    def test_returns_failed_on_non_204_status(self) -> None:
        """Non-204 status code should produce passed=False with error_type='config'."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_response(
                "invoke",
                {"StatusCode": 403},
                expected_params={
                    "FunctionName": "my-function",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("my-function", session)

        assert result.passed is False
        assert result.error_type == "config"
        assert result.resource_name == "my-function"
        assert result.resource_type == "lambda"
        assert "403" in result.error_message

    def test_access_denied_classified_as_auth(self) -> None:
        """AccessDeniedException should be classified as error_type='auth'."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_client_error(
                "invoke",
                service_error_code="AccessDeniedException",
                service_message="User is not authorized to perform lambda:InvokeFunction",
                expected_params={
                    "FunctionName": "my-function",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("my-function", session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert "AccessDeniedException" in result.error_message

    def test_expired_token_classified_as_auth(self) -> None:
        """ExpiredTokenException should be classified as error_type='auth'."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_client_error(
                "invoke",
                service_error_code="ExpiredTokenException",
                service_message="The security token included in the request is expired",
                expected_params={
                    "FunctionName": "my-function",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("my-function", session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert "ExpiredTokenException" in result.error_message

    def test_resource_not_found_classified_as_config(self) -> None:
        """ResourceNotFoundException should be classified as error_type='config'."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_client_error(
                "invoke",
                service_error_code="ResourceNotFoundException",
                service_message="Function not found: arn:aws:lambda:ap-southeast-2:123456789012:function:my-function",
                expected_params={
                    "FunctionName": "my-function",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("my-function", session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "ResourceNotFoundException" in result.error_message

    def test_generic_exception_classified_as_config(self) -> None:
        """Non-ClientError exceptions should be classified as error_type='config'."""
        session = boto3.Session(region_name="ap-southeast-2")
        mock_client = MagicMock()
        mock_client.invoke.side_effect = ConnectionError("Network timeout")

        with patch.object(session, "client", return_value=mock_client):
            result = check_lambda_invocable("my-function", session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "Network timeout" in result.error_message

    def test_result_includes_function_name(self) -> None:
        """The result should always include the function name as resource_name."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_response(
                "invoke",
                {"StatusCode": 204},
                expected_params={
                    "FunctionName": "arn:aws:lambda:ap-southeast-2:123456789012:function:test-fn",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable(
                    "arn:aws:lambda:ap-southeast-2:123456789012:function:test-fn",
                    session,
                )

        assert result.resource_name == "arn:aws:lambda:ap-southeast-2:123456789012:function:test-fn"
        assert result.resource_type == "lambda"

    def test_invalid_parameter_classified_as_config(self) -> None:
        """InvalidParameterValueException should be classified as error_type='config'."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_client_error(
                "invoke",
                service_error_code="InvalidParameterValueException",
                service_message="Invalid function name",
                expected_params={
                    "FunctionName": "bad-function-config",
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable("bad-function-config", session)

        assert result.passed is False
        assert result.error_type == "config"
        assert "InvalidParameterValueException" in result.error_message
