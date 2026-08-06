"""Property-based tests for smoke test error classification.

# Feature: deployment-integration-tests, Property 12: Smoke Test Error Classification

**Validates: Requirements 8.7, 8.8**

For any boto3 exception raised during a smoke test, the smoke test SHALL classify
`AccessDeniedException` and `ExpiredTokenException` as `error_type="auth"` and all
other failures (ResourceNotFoundException, InvalidParameterException, etc.) as
`error_type="config"`, and SHALL include the resource name, resource type, and
original error message in the result.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import boto3
from botocore.exceptions import ClientError
from botocore.stub import Stubber
from hypothesis import given, settings
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.smoke.lambda_check import check_lambda_invocable
from orcabus_pipeline_test_utils.smoke.sfn_check import check_state_machine_active
from orcabus_pipeline_test_utils.smoke.ssm_check import check_ssm_parameters_exist


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Auth error codes that should be classified as error_type="auth"
AUTH_ERROR_CODES = ["AccessDeniedException", "ExpiredTokenException"]

# Non-auth error codes that should be classified as error_type="config"
NON_AUTH_ERROR_CODES = [
    "ResourceNotFoundException",
    "InvalidParameterException",
    "InvalidParameterValueException",
    "ServiceException",
    "TooManyRequestsException",
    "InvalidRequestContentException",
    "RequestTooLargeException",
    "ResourceConflictException",
    "StateMachineDoesNotExist",
    "ParameterNotFound",
    "InternalServerError",
    "ThrottlingException",
    "ValidationException",
]

# Strategy: generate auth error codes
auth_error_code_st = st.sampled_from(AUTH_ERROR_CODES)

# Strategy: generate non-auth error codes
non_auth_error_code_st = st.sampled_from(NON_AUTH_ERROR_CODES)

# Strategy: generate error messages
error_message_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .:/-_",
    min_size=5,
    max_size=100,
)

# Strategy: generate resource names (function names, ARNs, SSM paths)
resource_name_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_/:",
    min_size=3,
    max_size=60,
)

# Strategy: smoke check type
smoke_check_type_st = st.sampled_from(["lambda", "state_machine", "ssm_parameter"])


def _make_client_error(error_code: str, error_message: str) -> ClientError:
    """Create a botocore ClientError with the given code and message."""
    return ClientError(
        error_response={
            "Error": {
                "Code": error_code,
                "Message": error_message,
            }
        },
        operation_name="TestOperation",
    )


# ---------------------------------------------------------------------------
# Property Tests
# ---------------------------------------------------------------------------


class TestSmokeTestErrorClassificationProperty:
    """Property 12: Smoke Test Error Classification.

    For any boto3 exception raised during a smoke test, the smoke test SHALL
    classify AccessDeniedException and ExpiredTokenException as error_type="auth"
    and all other failures as error_type="config", and SHALL include the resource
    name, resource type, and original error message in the result.
    """

    @given(
        error_code=auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_auth_errors_classified_as_auth_for_lambda(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Auth error codes produce error_type='auth' for Lambda checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.invoke.side_effect = _make_client_error(error_code, error_message)
        session.client.return_value = mock_client

        result = check_lambda_invocable(resource_name, session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert result.resource_name == resource_name
        assert result.resource_type == "lambda"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=non_auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_non_auth_errors_classified_as_config_for_lambda(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Non-auth error codes produce error_type='config' for Lambda checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.invoke.side_effect = _make_client_error(error_code, error_message)
        session.client.return_value = mock_client

        result = check_lambda_invocable(resource_name, session)

        assert result.passed is False
        assert result.error_type == "config"
        assert result.resource_name == resource_name
        assert result.resource_type == "lambda"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_auth_errors_classified_as_auth_for_sfn(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Auth error codes produce error_type='auth' for Step Function checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.describe_state_machine.side_effect = _make_client_error(
            error_code, error_message
        )
        session.client.return_value = mock_client

        result = check_state_machine_active(resource_name, session)

        assert result.passed is False
        assert result.error_type == "auth"
        assert result.resource_name == resource_name
        assert result.resource_type == "state_machine"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=non_auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_non_auth_errors_classified_as_config_for_sfn(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Non-auth error codes produce error_type='config' for Step Function checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.describe_state_machine.side_effect = _make_client_error(
            error_code, error_message
        )
        session.client.return_value = mock_client

        result = check_state_machine_active(resource_name, session)

        assert result.passed is False
        assert result.error_type == "config"
        assert result.resource_name == resource_name
        assert result.resource_type == "state_machine"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_auth_errors_classified_as_auth_for_ssm(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Auth error codes produce error_type='auth' for SSM checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.get_parameter.side_effect = _make_client_error(
            error_code, error_message
        )
        session.client.return_value = mock_client

        results = check_ssm_parameters_exist([resource_name], session)

        assert len(results) == 1
        result = results[0]
        assert result.passed is False
        assert result.error_type == "auth"
        assert result.resource_name == resource_name
        assert result.resource_type == "ssm_parameter"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=non_auth_error_code_st,
        error_message=error_message_st,
        resource_name=resource_name_st,
    )
    @settings(max_examples=100)
    def test_non_auth_errors_classified_as_config_for_ssm(
        self, error_code: str, error_message: str, resource_name: str
    ):
        """Non-auth error codes produce error_type='config' for SSM checks."""
        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        mock_client.get_parameter.side_effect = _make_client_error(
            error_code, error_message
        )
        session.client.return_value = mock_client

        results = check_ssm_parameters_exist([resource_name], session)

        assert len(results) == 1
        result = results[0]
        assert result.passed is False
        assert result.error_type == "config"
        assert result.resource_name == resource_name
        assert result.resource_type == "ssm_parameter"
        assert result.error_message is not None
        assert error_message in result.error_message

    @given(
        error_code=st.sampled_from(AUTH_ERROR_CODES + NON_AUTH_ERROR_CODES),
        error_message=error_message_st,
        resource_name=resource_name_st,
        check_type=smoke_check_type_st,
    )
    @settings(max_examples=100)
    def test_error_classification_is_consistent_across_resource_types(
        self,
        error_code: str,
        error_message: str,
        resource_name: str,
        check_type: str,
    ):
        """The same error code produces the same classification regardless of resource type."""
        expected_error_type = "auth" if error_code in AUTH_ERROR_CODES else "config"

        session = MagicMock(spec=boto3.Session)
        mock_client = MagicMock()
        client_error = _make_client_error(error_code, error_message)

        if check_type == "lambda":
            mock_client.invoke.side_effect = client_error
            session.client.return_value = mock_client
            result = check_lambda_invocable(resource_name, session)
        elif check_type == "state_machine":
            mock_client.describe_state_machine.side_effect = client_error
            session.client.return_value = mock_client
            result = check_state_machine_active(resource_name, session)
        else:  # ssm_parameter
            mock_client.get_parameter.side_effect = client_error
            session.client.return_value = mock_client
            results = check_ssm_parameters_exist([resource_name], session)
            result = results[0]

        assert result.passed is False
        assert result.error_type == expected_error_type
        assert result.resource_name == resource_name
        assert result.error_message is not None
