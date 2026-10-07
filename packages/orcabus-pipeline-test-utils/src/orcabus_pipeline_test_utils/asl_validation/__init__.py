"""ASL (Amazon States Language) validation engine.

Provides:
- validator: Structural validation of ASL definitions
- placeholder_resolver: ${__xxx__} placeholder substitution
- reference_checker: State and Lambda ARN reference validation
"""

from orcabus_pipeline_test_utils.asl_validation.placeholder_resolver import (
    load_placeholder_map,
    resolve_placeholders,
)
from orcabus_pipeline_test_utils.asl_validation.reference_checker import (
    check_lambda_arn_references,
    check_state_references,
)
from orcabus_pipeline_test_utils.asl_validation.validator import (
    ValidationCategory,
    ValidationResult,
    validate_asl_definition,
)

__all__ = [
    "ValidationCategory",
    "ValidationResult",
    "check_lambda_arn_references",
    "check_state_references",
    "load_placeholder_map",
    "resolve_placeholders",
    "validate_asl_definition",
]
