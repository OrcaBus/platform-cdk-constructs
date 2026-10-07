"""Post-deployment smoke test utilities.

Provides:
- lambda_check: Lambda DryRun invocation checker
- sfn_check: DescribeStateMachine checker
- ssm_check: SSM parameter existence checker
"""

from dataclasses import dataclass


@dataclass
class SmokeTestResult:
    """Result of a single smoke test check against a deployed AWS resource."""

    resource_name: str
    resource_type: str  # "lambda" | "state_machine" | "ssm_parameter"
    passed: bool
    error_type: str | None  # "auth" | "config" | None
    error_message: str | None
