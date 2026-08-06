"""SSM parameter existence checker.

Verifies each SSM parameter exists and is readable via GetParameter.
Returns list of SmokeTestResult with error classification per parameter.
"""

from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

from orcabus_pipeline_test_utils.smoke import SmokeTestResult

# Exception codes classified as authentication/authorization errors
_AUTH_ERROR_CODES = {"AccessDeniedException", "ExpiredTokenException"}


def check_ssm_parameters_exist(
    parameter_paths: list[str],
    session: boto3.Session,
) -> list[SmokeTestResult]:
    """Verify each SSM parameter exists and is readable.

    Calls ssm:GetParameter for each path and returns a SmokeTestResult per parameter.

    Error classification:
        - AccessDeniedException / ExpiredTokenException → error_type="auth"
        - All other failures → error_type="config"

    Args:
        parameter_paths: List of SSM parameter paths to verify.
        session: A boto3 Session configured for the target environment.

    Returns:
        A list of SmokeTestResult, one per parameter path.
    """
    client = session.client("ssm")
    results: list[SmokeTestResult] = []

    for path in parameter_paths:
        try:
            client.get_parameter(Name=path, WithDecryption=True)
            results.append(
                SmokeTestResult(
                    resource_name=path,
                    resource_type="ssm_parameter",
                    passed=True,
                    error_type=None,
                    error_message=None,
                )
            )
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_message = exc.response["Error"].get("Message", str(exc))
            error_type = "auth" if error_code in _AUTH_ERROR_CODES else "config"

            results.append(
                SmokeTestResult(
                    resource_name=path,
                    resource_type="ssm_parameter",
                    passed=False,
                    error_type=error_type,
                    error_message=error_message,
                )
            )

    return results
