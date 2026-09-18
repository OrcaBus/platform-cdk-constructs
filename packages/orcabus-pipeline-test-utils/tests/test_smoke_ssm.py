"""Unit tests for SSM parameter existence checker."""

from __future__ import annotations

import boto3
import pytest
from moto import mock_aws

from orcabus_pipeline_test_utils.smoke import SmokeTestResult
from orcabus_pipeline_test_utils.smoke.ssm_check import check_ssm_parameters_exist


@pytest.fixture
def ssm_session():
    """Provide a moto-mocked boto3 session with SSM available."""
    with mock_aws():
        session = boto3.Session(region_name="ap-southeast-2")
        yield session


@pytest.fixture
def ssm_session_with_params(ssm_session):
    """Create a session with some pre-existing SSM parameters."""
    client = ssm_session.client("ssm")
    client.put_parameter(
        Name="/orcabus/workflows/test/param-a",
        Value="value-a",
        Type="String",
        Overwrite=True,
    )
    client.put_parameter(
        Name="/orcabus/workflows/test/param-b",
        Value="secret-value",
        Type="SecureString",
        Overwrite=True,
    )
    return ssm_session


class TestCheckSsmParametersExist:
    """Tests for check_ssm_parameters_exist function."""

    def test_empty_parameter_list_returns_empty_results(self, ssm_session):
        """Passing an empty list returns no results."""
        results = check_ssm_parameters_exist([], ssm_session)
        assert results == []

    def test_existing_parameters_return_passed(self, ssm_session_with_params):
        """Parameters that exist should return passed=True."""
        results = check_ssm_parameters_exist(
            ["/orcabus/workflows/test/param-a", "/orcabus/workflows/test/param-b"],
            ssm_session_with_params,
        )
        assert len(results) == 2
        for result in results:
            assert result.passed is True
            assert result.error_type is None
            assert result.error_message is None
            assert result.resource_type == "ssm_parameter"

    def test_nonexistent_parameter_returns_failed_config(self, ssm_session):
        """A parameter that does not exist should return passed=False with error_type='config'."""
        results = check_ssm_parameters_exist(
            ["/orcabus/workflows/test/nonexistent"],
            ssm_session,
        )
        assert len(results) == 1
        result = results[0]
        assert result.passed is False
        assert result.resource_name == "/orcabus/workflows/test/nonexistent"
        assert result.resource_type == "ssm_parameter"
        assert result.error_type == "config"
        assert result.error_message is not None

    def test_mix_of_existing_and_nonexistent(self, ssm_session_with_params):
        """Results correctly reflect mixed existing and nonexistent parameters."""
        results = check_ssm_parameters_exist(
            [
                "/orcabus/workflows/test/param-a",
                "/orcabus/workflows/test/missing",
                "/orcabus/workflows/test/param-b",
            ],
            ssm_session_with_params,
        )
        assert len(results) == 3
        # First: exists
        assert results[0].passed is True
        assert results[0].resource_name == "/orcabus/workflows/test/param-a"
        # Second: missing
        assert results[1].passed is False
        assert results[1].resource_name == "/orcabus/workflows/test/missing"
        assert results[1].error_type == "config"
        # Third: exists
        assert results[2].passed is True
        assert results[2].resource_name == "/orcabus/workflows/test/param-b"

    def test_resource_name_matches_parameter_path(self, ssm_session_with_params):
        """The resource_name in results should match the input parameter path."""
        paths = ["/orcabus/workflows/test/param-a"]
        results = check_ssm_parameters_exist(paths, ssm_session_with_params)
        assert results[0].resource_name == "/orcabus/workflows/test/param-a"

    def test_secure_string_parameter_readable(self, ssm_session_with_params):
        """SecureString parameters should be readable (WithDecryption=True)."""
        results = check_ssm_parameters_exist(
            ["/orcabus/workflows/test/param-b"],
            ssm_session_with_params,
        )
        assert len(results) == 1
        assert results[0].passed is True

    def test_result_is_smoke_test_result_type(self, ssm_session_with_params):
        """Results should be instances of SmokeTestResult."""
        results = check_ssm_parameters_exist(
            ["/orcabus/workflows/test/param-a"],
            ssm_session_with_params,
        )
        assert isinstance(results[0], SmokeTestResult)

    def test_one_result_per_parameter(self, ssm_session_with_params):
        """The number of results should equal the number of input parameter paths."""
        paths = [
            "/orcabus/workflows/test/param-a",
            "/orcabus/workflows/test/param-b",
            "/orcabus/workflows/test/missing-1",
            "/orcabus/workflows/test/missing-2",
        ]
        results = check_ssm_parameters_exist(paths, ssm_session_with_params)
        assert len(results) == len(paths)
