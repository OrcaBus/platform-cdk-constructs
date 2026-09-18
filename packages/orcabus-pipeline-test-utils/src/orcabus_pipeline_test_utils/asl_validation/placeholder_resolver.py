"""Placeholder resolver for ASL templates.

Resolves ${__xxx__} placeholders in ASL content with valid dummy ARNs
or user-provided placeholder maps.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


# Regex to match ${__xxx__} placeholders in ASL content
PLACEHOLDER_PATTERN = re.compile(r"\$\{__([a-z0-9_]+)__\}")

# Default region and account used for dummy ARN generation
DEFAULT_REGION = "ap-southeast-2"
DEFAULT_ACCOUNT_ID = "123456789012"


def resolve_placeholders(
    asl_content: str,
    placeholder_map: dict[str, str] | None = None,
) -> str:
    """Replace ${__xxx__} placeholders with valid dummy ARN values.

    If placeholder_map is None, auto-generates dummy ARNs based on
    placeholder names (e.g., ${__lambda_function_arn__} ->
    arn:aws:lambda:ap-southeast-2:123456789012:function:lambda_function).

    Args:
        asl_content: Raw ASL JSON string containing placeholders.
        placeholder_map: Optional mapping from full placeholder tokens
            (e.g., "${__my_lambda_function_arn__}") to replacement values.
            If None, dummy values are auto-generated from placeholder names.

    Returns:
        ASL content string with all placeholders resolved.
    """
    if placeholder_map is None:
        placeholder_map = {}

    def _replace_match(match: re.Match[str]) -> str:
        full_token = match.group(0)  # e.g., ${__lambda_function_arn__}
        inner_name = match.group(1)  # e.g., lambda_function_arn

        # Check explicit map first (using the full token as key)
        if full_token in placeholder_map:
            return placeholder_map[full_token]

        # Auto-generate a dummy value based on the placeholder name pattern
        return _generate_dummy_value(inner_name)

    return PLACEHOLDER_PATTERN.sub(_replace_match, asl_content)


def load_placeholder_map(path: str | Path) -> dict[str, str]:
    """Load a placeholder map from a JSON file.

    The JSON file should contain a flat object mapping placeholder tokens
    to their replacement values, e.g.:
    {
        "${__lambda_function_arn__}": "arn:aws:lambda:...:function:my-fn",
        "${__event_bus_name__}": "my-event-bus"
    }

    Args:
        path: Path to the JSON file containing the placeholder map.

    Returns:
        Dictionary mapping placeholder tokens to replacement values.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    file_path = Path(path)
    with file_path.open("r") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(
            f"Placeholder map file must contain a JSON object, got {type(data).__name__}"
        )

    return data


def _generate_dummy_value(inner_name: str) -> str:
    """Generate a dummy replacement value based on the placeholder name pattern.

    Recognises common patterns in OrcaBus ASL templates:
    - *_lambda_function_arn -> Lambda ARN
    - *_state_machine_arn -> State Machine ARN
    - *_event_bus_name / event_bus_name -> EventBridge bus name
    - *_ssm_parameter_name / *_ssm_parameter_path_prefix -> SSM path
    - *_detail_type -> EventBridge detail type string
    - *_status -> Status string
    - *_version -> Version string
    - stack_source -> Event source string
    - workflow_name -> Workflow name string

    Args:
        inner_name: The name extracted from between ${__...__} delimiters.

    Returns:
        A valid dummy value appropriate for the placeholder type.
    """
    # Lambda function ARN
    if inner_name.endswith("_lambda_function_arn"):
        # Strip the _lambda_function_arn suffix to get the function name
        fn_name = inner_name.removesuffix("_lambda_function_arn")
        return (
            f"arn:aws:lambda:{DEFAULT_REGION}:{DEFAULT_ACCOUNT_ID}"
            f":function:{fn_name}"
        )

    # State machine ARN
    if inner_name.endswith("_state_machine_arn"):
        sm_name = inner_name.removesuffix("_state_machine_arn")
        return (
            f"arn:aws:states:{DEFAULT_REGION}:{DEFAULT_ACCOUNT_ID}"
            f":stateMachine:{sm_name}"
        )

    # EventBridge event bus
    if inner_name == "event_bus_name" or inner_name.endswith("_event_bus_name"):
        bus_name = inner_name.removesuffix("_event_bus_name") or "default"
        return (
            f"arn:aws:events:{DEFAULT_REGION}:{DEFAULT_ACCOUNT_ID}"
            f":event-bus/{bus_name}"
        )

    # SSM parameter path prefix (both _ssm_parameter_path_prefix and _ssm_parameter_prefix)
    if inner_name.endswith("_ssm_parameter_path_prefix"):
        param_name = inner_name.removesuffix("_ssm_parameter_path_prefix")
        return f"/test/{param_name.replace('_', '/')}"

    if inner_name.endswith("_ssm_parameter_prefix"):
        param_name = inner_name.removesuffix("_ssm_parameter_prefix")
        return f"/test/{param_name.replace('_', '/')}"

    # SSM parameter name
    if inner_name.endswith("_ssm_parameter_name"):
        param_name = inner_name.removesuffix("_ssm_parameter_name")
        return f"/test/{param_name.replace('_', '/')}"

    # EventBridge detail type
    if inner_name.endswith("_detail_type"):
        detail_name = inner_name.removesuffix("_detail_type")
        return detail_name.replace("_", ".")

    # Status strings (e.g., draft_status, ready_event_status, draft_event_status)
    if inner_name.endswith("_status"):
        status_name = inner_name.removesuffix("_status")
        # Take only the last meaningful word for the status value
        # e.g., "draft_event" -> "DRAFT", "ready_event" -> "READY"
        parts = status_name.split("_")
        # Use the first part as the status (typically "draft" or "ready")
        return parts[0].upper()

    # Version strings
    if inner_name.endswith("_version") or inner_name.startswith("default_payload_version"):
        return "1.0.0"

    # S3 bucket names
    if inner_name.endswith("_bucket"):
        bucket_name = inner_name.removesuffix("_bucket")
        return f"test-{bucket_name.replace('_', '-')}-bucket"

    # URI values (e.g., pipeline_cache_uri)
    if inner_name.endswith("_uri"):
        path_name = inner_name.removesuffix("_uri")
        return f"s3://test-bucket/{path_name.replace('_', '-')}/"

    # Stack source
    if inner_name == "stack_source":
        return "orcabus.test"

    # Workflow name
    if inner_name == "workflow_name":
        return "test-workflow"

    # Generic fallback — return the inner name as a plain string value
    # This ensures no placeholder is left unresolved
    return inner_name.replace("_", "-")
