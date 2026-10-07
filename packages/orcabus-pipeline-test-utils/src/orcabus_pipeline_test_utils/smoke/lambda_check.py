"""Lambda DryRun invocation checker.

Performs InvocationType: DryRun invocation via boto3 and returns
SmokeTestResult with passed=True on HTTP 204, passed=False otherwise.
Classifies AccessDeniedException/ExpiredTokenException as error_type="auth",
all other failures as error_type="config".
"""

from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

from orcabus_pipeline_test_utils.smoke import SmokeTestResult

# Exceptions classified as authentication/authorization errors
_AUTH_ERROR_CODES = {"AccessDeniedException", "ExpiredTokenException"}


def check_lambda_invocable(
    function_name: str,
    session: boto3.Session,
) -> SmokeTestResult:
    """Perform a DryRun invocation of a Lambda function and verify HTTP 204.

    A DryRun invocation validates that the caller has permission to invoke
    the function and that the function configuration is valid, without
    actually executing the function code.

    Args:
        function_name: The name or ARN of the Lambda function to check.
        session: A boto3 Session configured with appropriate credentials.

    Returns:
        SmokeTestResult with passed=True if HTTP 204 is returned,
        passed=False with error classification otherwise.
    """
    client = session.client("lambda")

    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType="DryRun",
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        error_type = "auth" if error_code in _AUTH_ERROR_CODES else "config"

        return SmokeTestResult(
            resource_name=function_name,
            resource_type="lambda",
            passed=False,
            error_type=error_type,
            error_message=f"{error_code}: {error_message}",
        )
    except Exception as e:
        # Catch non-ClientError exceptions (network timeouts, etc.)
        return SmokeTestResult(
            resource_name=function_name,
            resource_type="lambda",
            passed=False,
            error_type="config",
            error_message=str(e),
        )

    status_code = response.get("StatusCode", 0)

    if status_code == 204:
        return SmokeTestResult(
            resource_name=function_name,
            resource_type="lambda",
            passed=True,
            error_type=None,
            error_message=None,
        )

    return SmokeTestResult(
        resource_name=function_name,
        resource_type="lambda",
        passed=False,
        error_type="config",
        error_message=f"Expected HTTP 204, got {status_code}",
    )
