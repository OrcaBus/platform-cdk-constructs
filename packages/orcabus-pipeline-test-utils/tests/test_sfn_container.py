"""Unit tests for SfnLocalContainer Docker lifecycle manager."""

from __future__ import annotations

import socket
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest
from docker.errors import NotFound as DockerNotFound

from orcabus_pipeline_test_utils.sfn_local.container import (
    SfnLocalContainer,
    SfnLocalContainerError,
    _CONTAINER_NAME_PREFIX,
    _HEALTH_CHECK_TIMEOUT,
    _MOCK_CONFIG_CONTAINER_PATH,
)


@pytest.fixture
def mock_config_file(tmp_path: Path) -> Path:
    """Create a temporary MockConfigFile.json for testing."""
    config_file = tmp_path / "MockConfigFile.json"
    config_file.write_text('{"StateMachines": {}, "MockedResponses": {}}')
    return config_file


class TestSfnLocalContainerInit:
    """Test SfnLocalContainer initialization."""

    def test_init_with_valid_mock_config(self, mock_config_file: Path) -> None:
        container = SfnLocalContainer(str(mock_config_file))
        assert container.port == 8083
        assert container.endpoint_url == "http://localhost:8083"

    def test_init_with_custom_port(self, mock_config_file: Path) -> None:
        container = SfnLocalContainer(str(mock_config_file), port=9999)
        assert container.port == 9999
        assert container.endpoint_url == "http://localhost:9999"

    def test_init_with_missing_mock_config_raises(self, tmp_path: Path) -> None:
        missing_path = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError, match="MockConfigFile.json not found"):
            SfnLocalContainer(str(missing_path))

    def test_init_resolves_relative_path(self, mock_config_file: Path) -> None:
        container = SfnLocalContainer(str(mock_config_file))
        assert container._mock_config_path.is_absolute()


class TestSfnLocalContainerStart:
    """Test SfnLocalContainer.start() method."""

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_raises_when_docker_unavailable(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        from docker.errors import DockerException

        mock_from_env.side_effect = DockerException("Docker not running")
        container = SfnLocalContainer(str(mock_config_file))

        with pytest.raises(SfnLocalContainerError, match="Docker is not available"):
            container.start()

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_raises_when_ping_fails(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        from docker.errors import DockerException

        mock_client = MagicMock()
        mock_client.ping.side_effect = DockerException("Ping failed")
        mock_from_env.return_value = mock_client
        container = SfnLocalContainer(str(mock_config_file))

        with pytest.raises(SfnLocalContainerError, match="Docker is not available"):
            container.start()

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_succeeds_with_healthy_container(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        # Mock the health check to succeed immediately
        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        mock_client.containers.run.assert_called_once()
        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["ports"] == {"8083/tcp": 8083}
        assert str(mock_config_file.resolve()) in call_kwargs["volumes"]

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_raises_on_health_check_timeout(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.logs.return_value = b"Container startup log"
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=False):
            with pytest.raises(
                SfnLocalContainerError, match="failed health check"
            ):
                container.start()

        # Verify container is cleaned up on failure
        mock_container.stop.assert_called()

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_mounts_mock_config_read_only(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        call_kwargs = mock_client.containers.run.call_args[1]
        volume_config = call_kwargs["volumes"][str(mock_config_file.resolve())]
        assert volume_config["bind"] == _MOCK_CONFIG_CONTAINER_PATH
        assert volume_config["mode"] == "ro"

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_sets_sfn_mock_config_env(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["environment"]["SFN_MOCK_CONFIG"] == _MOCK_CONFIG_CONTAINER_PATH

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_start_cleans_up_existing_container(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_existing = MagicMock()
        mock_client.containers.get.return_value = mock_existing
        mock_new_container = MagicMock()
        mock_client.containers.run.return_value = mock_new_container
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        mock_existing.stop.assert_called_once()
        mock_existing.remove.assert_called_once_with(force=True)


class TestSfnLocalContainerStop:
    """Test SfnLocalContainer.stop() method."""

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_stop_removes_container(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        container.stop()
        mock_container.stop.assert_called_with(timeout=5)
        mock_container.remove.assert_called_with(force=True)

    def test_stop_safe_when_never_started(self, mock_config_file: Path) -> None:
        container = SfnLocalContainer(str(mock_config_file))
        # Should not raise
        container.stop()

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_stop_handles_already_removed_container(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        from docker.errors import NotFound

        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.stop.side_effect = NotFound("already gone")
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            container.start()

        # Should not raise even when container is already gone
        container.stop()


class TestSfnLocalContainerHealthCheck:
    """Test SfnLocalContainer.is_healthy() method."""

    def test_is_healthy_returns_false_when_not_running(
        self, mock_config_file: Path
    ) -> None:
        container = SfnLocalContainer(str(mock_config_file), port=19999)
        # No service listening on this port
        assert container.is_healthy() is False

    @patch(
        "orcabus_pipeline_test_utils.sfn_local.container.socket.create_connection"
    )
    def test_is_healthy_returns_true_when_port_open(
        self, mock_conn: MagicMock, mock_config_file: Path
    ) -> None:
        mock_socket = MagicMock()
        mock_conn.return_value.__enter__ = MagicMock(return_value=mock_socket)
        mock_conn.return_value.__exit__ = MagicMock(return_value=False)

        container = SfnLocalContainer(str(mock_config_file))
        assert container.is_healthy() is True

    @patch(
        "orcabus_pipeline_test_utils.sfn_local.container.socket.create_connection"
    )
    def test_is_healthy_returns_false_on_connection_refused(
        self, mock_conn: MagicMock, mock_config_file: Path
    ) -> None:
        mock_conn.side_effect = ConnectionRefusedError("refused")

        container = SfnLocalContainer(str(mock_config_file))
        assert container.is_healthy() is False


class TestSfnLocalContainerContextManager:
    """Test SfnLocalContainer as a context manager."""

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_context_manager_starts_and_stops(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with patch.object(container, "_wait_for_healthy", return_value=True):
            with container as ctx:
                assert ctx is container
                assert ctx.endpoint_url == "http://localhost:8083"

        mock_container.stop.assert_called()
        mock_container.remove.assert_called()

    @patch("orcabus_pipeline_test_utils.sfn_local.container.docker.from_env")
    def test_context_manager_stops_on_exception(
        self, mock_from_env: MagicMock, mock_config_file: Path
    ) -> None:
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_client.containers.get.side_effect = DockerNotFound("not found")
        mock_from_env.return_value = mock_client

        container = SfnLocalContainer(str(mock_config_file))

        with pytest.raises(RuntimeError):
            with patch.object(container, "_wait_for_healthy", return_value=True):
                with container:
                    raise RuntimeError("test error")

        mock_container.stop.assert_called()
        mock_container.remove.assert_called()
