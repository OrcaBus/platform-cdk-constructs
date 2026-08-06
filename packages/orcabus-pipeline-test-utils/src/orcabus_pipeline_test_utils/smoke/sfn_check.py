"""State Machine checker.

Calls DescribeStateMachine and verifies status=ACTIVE with non-null definition.
Returns SmokeTestResult with appropriate error classification.
"""

from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

from orcabus_pipeline_test_utils.smoke import SmokeTestResult

# Auth-related error codes that indicate IAM/credential issues
_AUTH_ERROR_CODES = {"AccessDeniedException", "ExpiredTokenException"}


def check_state_machine_active(
    state_machine_arn: str,
    session: boto3.Session,
) -> SmokeTestResult:
    """Call DescribeStateMachine, verify status=ACTIVE and definition non-null.

    Args:
        state_machine_arn: The full ARN of the Step Functions state machine.
        session: A boto3 Session configured for the target environment.

    Returns:
        SmokeTestResult with passed=True if the state machine is ACTIVE with
        a non-null definition, or passed=False with error details otherwise.
    """
    client = session.client("stepfunctions")

    try:
        response = client.describe_state_machine(stateMachineArn=state_machine_arn)
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        error_message = exc.response["Error"]["Message"]
        error_type = "auth" if error_code in _AUTH_ERROR_CODES else "config"
        return SmokeTestResult(
            resource_name=state_machine_arn,
            resource_type="state_machine",
            passed=False,
            error_type=error_type,
            error_message=f"{error_code}: {error_message}",
        )
    except Exception as exc:
        return SmokeTestResult(
            resource_name=state_machine_arn,
            resource_type="state_machine",
            passed=False,
            error_type="config",
            error_message=str(exc),
        )

    status = response.get("status")
    definition = response.get("definition")

    if status != "ACTIVE":
        return SmokeTestResult(
            resource_name=state_machine_arn,
            resource_type="state_machine",
            passed=False,
            error_type="config",
            error_message=f"State machine status is '{status}', expected 'ACTIVE'",
        )

    if not definition:
        return SmokeTestResult(
            resource_name=state_machine_arn,
            resource_type="state_machine",
            passed=False,
            error_type="config",
            error_message="State machine definition is null or empty",
        )

    return SmokeTestResult(
        resource_name=state_machine_arn,
        resource_type="state_machine",
        passed=True,
        error_type=None,
        error_message=None,
    )
