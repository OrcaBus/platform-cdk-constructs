"""Property-based tests for smoke check resource validation.

# Feature: deployment-integration-tests, Property 11: Smoke Check Resource Validation

**Validates: Requirements 8.3, 8.4, 8.5**

For any AWS resource check (Lambda DryRun, DescribeStateMachine, or SSM GetParameter)
and any mocked boto3 response, the corresponding smoke check function SHALL return
`passed=True` only when the response indicates the resource is correctly configured
(HTTP 204 for Lambda, status=ACTIVE with non-null definition for state machines,
successful GetParameter for SSM), and SHALL return `passed=False` with a descriptive
`error_message` for all other responses.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import boto3
from botocore.exceptions import ClientError
from botocore.stub import Stubber
from hypothesis import given, settings
from hypothesis import strategies as st
from moto import mock_aws

from orcabus_pipeline_test_utils.smoke import SmokeTestResult
from orcabus_pipeline_test_utils.smoke.lambda_check import check_lambda_invocable
from orcabus_pipeline_test_utils.smoke.sfn_check import check_state_machine_active
from orcabus_pipeline_test_utils.smoke.ssm_check import check_ssm_parameters_exist


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# HTTP status codes: 204 is the only passing code for Lambda DryRun
http_status_code_st = st.integers(min_value=100, max_value=599)

# Non-empty function names / ARNs
function_name_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_",
    min_size=1,
    max_size=50,
)

# State machine ARN-like strings
state_machine_arn_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789:/-",
    min_size=1,
    max_size=80,
).map(lambda s: f"arn:aws:states:ap-southeast-2:123456789012:stateMachine:{s}")

# State machine statuses
sfn_status_st = st.sampled_from(["ACTIVE", "DELETING", "INACTIVE"])

# State machine definitions: non-null non-empty strings or empty/None
valid_definition_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz{}:\"',",
    min_size=1,
    max_size=100,
)

null_or_empty_definition_st = st.sampled_from([None, ""])

# SSM parameter paths
ssm_path_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789/-_",
    min_size=1,
    max_size=60,
).map(lambda s: f"/orcabus/test/{s}")


# ---------------------------------------------------------------------------
# Property Tests: Lambda DryRun
# ---------------------------------------------------------------------------


class TestLambdaDryRunResourceValidationProperty:
    """Property 11 (Lambda): passed=True only when HTTP 204 is returned."""

    @given(status_code=http_status_code_st, func_name=function_name_st)
    @settings(max_examples=100)
    def test_lambda_passed_iff_status_204(
        self, status_code: int, func_name: str
    ):
        """check_lambda_invocable returns passed=True if and only if HTTP 204."""
        session = boto3.Session(region_name="ap-southeast-2")
        client = session.client("lambda")

        with Stubber(client) as stubber:
            stubber.add_response(
                "invoke",
                {"StatusCode": status_code},
                expected_params={
                    "FunctionName": func_name,
                    "InvocationType": "DryRun",
                },
            )

            with patch.object(session, "client", return_value=client):
                result = check_lambda_invocable(func_name, session)

        assert result.resource_name == func_name
        assert result.resource_type == "lambda"

        if status_code == 204:
            assert result.passed is True, (
                f"Expected passed=True for HTTP 204, got passed=False "
                f"with error_message={result.error_message!r}"
            )
            assert result.error_type is None
            assert result.error_message is None
        else:
            assert result.passed is False, (
                f"Expected passed=False for HTTP {status_code}, got passed=True"
            )
            assert result.error_message is not None
            assert result.error_type == "config"

    @given(func_name=function_name_st)
    @settings(max_examples=100)
    def test_lambda_client_error_always_fails(self, func_name: str):
        """Any ClientError during Lambda invoke should result in passed=False."""
        session = boto3.Session(region_name="ap-southeast-2")
        mock_client = MagicMock()
        mock_client.invoke.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "ResourceNotFoundException",
                    "Message": f"Function not found: {func_name}",
                }
            },
            operation_name="Invoke",
        )

        with patch.object(session, "client", return_value=mock_client):
            result = check_lambda_invocable(func_name, session)

        assert result.passed is False
        assert result.resource_name == func_name
        assert result.resource_type == "lambda"
        assert result.error_message is not None
        assert len(result.error_message) > 0


# ---------------------------------------------------------------------------
# Property Tests: State Machine
# ---------------------------------------------------------------------------


class TestStateMachineResourceValidationProperty:
    """Property 11 (SFN): passed=True only when status=ACTIVE and definition is non-null/non-empty."""

    @given(
        sm_arn=state_machine_arn_st,
        status=sfn_status_st,
        definition=st.one_of(valid_definition_st, null_or_empty_definition_st),
    )
    @settings(max_examples=100)
    def test_sfn_passed_iff_active_with_definition(
        self, sm_arn: str, status: str, definition: str | None
    ):
        """check_state_machine_active returns passed=True iff status=ACTIVE and definition truthy."""
        session = MagicMock()
        mock_client = MagicMock()
        session.client.return_value = mock_client

        mock_client.describe_state_machine.return_value = {
            "stateMachineArn": sm_arn,
            "status": status,
            "definition": definition,
            "name": "test-sm",
        }

        result = check_state_machine_active(sm_arn, session)

        assert result.resource_name == sm_arn
        assert result.resource_type == "state_machine"

        should_pass = status == "ACTIVE" and bool(definition)

        if should_pass:
            assert result.passed is True, (
                f"Expected passed=True for status={status!r}, "
                f"definition={definition!r}, but got passed=False "
                f"with error_message={result.error_message!r}"
            )
            assert result.error_type is None
            assert result.error_message is None
        else:
            assert result.passed is False, (
                f"Expected passed=False for status={status!r}, "
                f"definition={definition!r}, but got passed=True"
            )
            assert result.error_type == "config"
            assert result.error_message is not None
            assert len(result.error_message) > 0

    @given(sm_arn=state_machine_arn_st)
    @settings(max_examples=100)
    def test_sfn_client_error_always_fails(self, sm_arn: str):
        """Any ClientError during DescribeStateMachine should result in passed=False."""
        session = MagicMock()
        mock_client = MagicMock()
        session.client.return_value = mock_client

        mock_client.describe_state_machine.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "StateMachineDoesNotExist",
                    "Message": "State machine does not exist",
                }
            },
            operation_name="DescribeStateMachine",
        )

        result = check_state_machine_active(sm_arn, session)

        assert result.passed is False
        assert result.resource_name == sm_arn
        assert result.resource_type == "state_machine"
        assert result.error_message is not None
        assert len(result.error_message) > 0


# ---------------------------------------------------------------------------
# Property Tests: SSM GetParameter
# ---------------------------------------------------------------------------


class TestSsmParameterResourceValidationProperty:
    """Property 11 (SSM): passed=True only when GetParameter succeeds."""

    @given(
        param_path=ssm_path_st,
        param_exists=st.booleans(),
    )
    @settings(max_examples=100, deadline=None)
    def test_ssm_passed_iff_get_parameter_succeeds(
        self, param_path: str, param_exists: bool
    ):
        """check_ssm_parameters_exist returns passed=True iff GetParameter succeeds."""
        with mock_aws():
            session = boto3.Session(region_name="ap-southeast-2")
            client = session.client("ssm")

            if param_exists:
                client.put_parameter(
                    Name=param_path,
                    Value="test-value",
                    Type="String",
                    Overwrite=True,
                )

            results = check_ssm_parameters_exist([param_path], session)

            assert len(results) == 1
            result = results[0]
            assert result.resource_name == param_path
            assert result.resource_type == "ssm_parameter"

            if param_exists:
                assert result.passed is True, (
                    f"Expected passed=True for existing param {param_path!r}, "
                    f"but got passed=False with error_message={result.error_message!r}"
                )
                assert result.error_type is None
                assert result.error_message is None
            else:
                assert result.passed is False, (
                    f"Expected passed=False for missing param {param_path!r}, "
                    f"but got passed=True"
                )
                assert result.error_type == "config"
                assert result.error_message is not None
                assert len(result.error_message) > 0

    @given(
        paths=st.lists(ssm_path_st, min_size=1, max_size=5, unique=True),
    )
    @settings(max_examples=100, deadline=None)
    def test_ssm_result_count_matches_input_count(self, paths: list[str]):
        """The number of results always equals the number of input paths."""
        with mock_aws():
            session = boto3.Session(region_name="ap-southeast-2")
            results = check_ssm_parameters_exist(paths, session)

            assert len(results) == len(paths)
            for result, path in zip(results, paths):
                assert result.resource_name == path
                assert result.resource_type == "ssm_parameter"
