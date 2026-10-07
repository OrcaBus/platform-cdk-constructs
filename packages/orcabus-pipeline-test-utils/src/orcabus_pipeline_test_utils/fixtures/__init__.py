"""Shared pytest fixtures for OrcaBus Pipeline Orchestrator tests.

Provides:
- aws_mocks: Session-scoped moto-based AWS client fixtures
- lambda_context: Mock Lambda context fixture
- event_builder: Event builder fixture for handler invocation
"""

from orcabus_pipeline_test_utils.fixtures.lambda_context import (
    MockLambdaContext,
    lambda_context,
)

__all__ = [
    "MockLambdaContext",
    "lambda_context",
]
