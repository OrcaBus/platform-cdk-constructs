"""Moto-based AWS mock fixtures.

Provides session-scoped pre-configured boto3 clients for:
- S3
- SSM Parameter Store
- Secrets Manager
- EventBridge

These fixtures use moto's `mock_aws` context manager (moto v5+ unified API)
to provide fully mocked AWS services for testing without hitting real AWS.
The session scope ensures mocks persist across all tests in a session,
improving test performance.
"""

import os

import boto3
import pytest
from moto import mock_aws

# Default AWS region matching OrcaBus deployment
AWS_DEFAULT_REGION = "ap-southeast-2"


@pytest.fixture(scope="session", autouse=True)
def _aws_credentials():
    """Set dummy AWS credentials for moto.

    Moto requires AWS credentials to be set in the environment,
    even though they are never used against real AWS services.
    This fixture sets them for the entire test session.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # noqa: S105  # pragma: allowlist secret
    os.environ["AWS_SECURITY_TOKEN"] = "testing"  # noqa: S105  # pragma: allowlist secret
    os.environ["AWS_SESSION_TOKEN"] = "testing"  # noqa: S105  # pragma: allowlist secret
    os.environ["AWS_DEFAULT_REGION"] = AWS_DEFAULT_REGION


@pytest.fixture(scope="session")
def mock_s3_client():
    """Provide a session-scoped mocked S3 boto3 client.

    Yields a boto3 S3 client operating against moto's in-memory
    S3 service. The mock is active for the entire test session.

    Yields:
        boto3.client: A mocked S3 client for the ap-southeast-2 region.
    """
    with mock_aws():
        client = boto3.client("s3", region_name=AWS_DEFAULT_REGION)
        yield client


@pytest.fixture(scope="session")
def mock_ssm_client():
    """Provide a session-scoped mocked SSM Parameter Store boto3 client.

    Yields a boto3 SSM client operating against moto's in-memory
    SSM service. The mock is active for the entire test session.

    Yields:
        boto3.client: A mocked SSM client for the ap-southeast-2 region.
    """
    with mock_aws():
        client = boto3.client("ssm", region_name=AWS_DEFAULT_REGION)
        yield client


@pytest.fixture(scope="session")
def mock_secretsmanager_client():
    """Provide a session-scoped mocked Secrets Manager boto3 client.

    Yields a boto3 Secrets Manager client operating against moto's
    in-memory Secrets Manager service. The mock is active for the
    entire test session.

    Yields:
        boto3.client: A mocked Secrets Manager client for the ap-southeast-2 region.
    """
    with mock_aws():
        client = boto3.client("secretsmanager", region_name=AWS_DEFAULT_REGION)
        yield client


@pytest.fixture(scope="session")
def mock_events_client():
    """Provide a session-scoped mocked EventBridge boto3 client.

    Yields a boto3 EventBridge (events) client operating against moto's
    in-memory EventBridge service. The mock is active for the entire
    test session.

    Yields:
        boto3.client: A mocked EventBridge client for the ap-southeast-2 region.
    """
    with mock_aws():
        client = boto3.client("events", region_name=AWS_DEFAULT_REGION)
        yield client
