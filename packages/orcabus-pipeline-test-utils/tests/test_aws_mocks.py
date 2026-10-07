"""Tests for AWS mock fixtures.

Verifies that the session-scoped moto fixtures provide working boto3 clients.
"""

import pytest


# Import the fixtures so pytest can discover them
from orcabus_pipeline_test_utils.fixtures.aws_mocks import (
    _aws_credentials,
    mock_s3_client,
    mock_ssm_client,
    mock_secretsmanager_client,
    mock_events_client,
)


class TestMockS3Client:
    """Tests for the mock_s3_client fixture."""

    def test_create_bucket(self, mock_s3_client):
        """Verify we can create and list buckets via the mocked S3 client."""
        mock_s3_client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
        )
        response = mock_s3_client.list_buckets()
        bucket_names = [b["Name"] for b in response["Buckets"]]
        assert "test-bucket" in bucket_names

    def test_put_and_get_object(self, mock_s3_client):
        """Verify we can put and get objects via the mocked S3 client."""
        mock_s3_client.create_bucket(
            Bucket="data-bucket",
            CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
        )
        mock_s3_client.put_object(
            Bucket="data-bucket",
            Key="test-key",
            Body=b"test-content",
        )
        response = mock_s3_client.get_object(Bucket="data-bucket", Key="test-key")
        assert response["Body"].read() == b"test-content"


class TestMockSSMClient:
    """Tests for the mock_ssm_client fixture."""

    def test_put_and_get_parameter(self, mock_ssm_client):
        """Verify we can put and get SSM parameters."""
        mock_ssm_client.put_parameter(
            Name="/orcabus/test/param",
            Value="test-value",
            Type="String",
        )
        response = mock_ssm_client.get_parameter(Name="/orcabus/test/param")
        assert response["Parameter"]["Value"] == "test-value"


class TestMockSecretsManagerClient:
    """Tests for the mock_secretsmanager_client fixture."""

    def test_create_and_get_secret(self, mock_secretsmanager_client):
        """Verify we can create and retrieve secrets."""
        mock_secretsmanager_client.create_secret(
            Name="test-secret",
            SecretString="super-secret-value",  # pragma: allowlist secret
        )
        response = mock_secretsmanager_client.get_secret_value(SecretId="test-secret")
        assert response["SecretString"] == "super-secret-value"


class TestMockEventsClient:
    """Tests for the mock_events_client fixture."""

    def test_put_events(self, mock_events_client):
        """Verify we can put events to EventBridge."""
        response = mock_events_client.put_events(
            Entries=[
                {
                    "Source": "orcabus.test",
                    "DetailType": "TestEvent",
                    "Detail": '{"key": "value"}',
                    "EventBusName": "default",
                }
            ]
        )
        assert response["FailedEntryCount"] == 0

    def test_create_event_bus(self, mock_events_client):
        """Verify we can create an event bus."""
        mock_events_client.create_event_bus(Name="OrcaBusMain")
        response = mock_events_client.list_event_buses()
        bus_names = [b["Name"] for b in response["EventBuses"]]
        assert "OrcaBusMain" in bus_names
