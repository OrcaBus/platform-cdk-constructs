"""Pytest plugin for OrcaBus Pipeline Test Utilities.

This module is auto-registered via the pytest11 entry point in pyproject.toml:

    [project.entry-points.pytest11]
    orcabus_pipeline_test_utils = "orcabus_pipeline_test_utils.conftest_plugin"

It exposes shared fixtures (AWS mocks, Lambda context, event builder) to all
tests in services that install this package — no explicit conftest imports needed.

When pytest discovers this plugin at startup, it imports all fixture functions
below, making them available to any test session automatically.
"""

# AWS mock fixtures (session-scoped, moto-based)
from orcabus_pipeline_test_utils.fixtures.aws_mocks import (  # noqa: F401
    _aws_credentials,
    mock_events_client,
    mock_s3_client,
    mock_secretsmanager_client,
    mock_ssm_client,
)

# Lambda context fixture
from orcabus_pipeline_test_utils.fixtures.lambda_context import (  # noqa: F401
    lambda_context,
)

# Event builder fixture
from orcabus_pipeline_test_utils.fixtures.event_builder import (  # noqa: F401
    event_builder,
)
