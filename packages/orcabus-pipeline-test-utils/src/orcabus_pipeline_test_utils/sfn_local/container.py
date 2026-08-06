"""Docker container lifecycle manager for Step Functions Local.

Manages the amazon/aws-stepfunctions-local Docker image with:
- start() with health check polling (max 30s)
- stop() with cleanup
- is_healthy() check
- MockConfigFile.json mounting
"""

from __future__ import annotations

import logging
import socket
import time
from pathlib import Path

import docker
from docker.errors import DockerException, NotFound
from docker.models.containers import Container

logger = logging.getLogger(__name__)

_IMAGE = "amazon/aws-stepfunctions-local"
_CONTAINER_NAME_PREFIX = "sfn-local-test"
_HEALTH_CHECK_TIMEOUT = 30  # seconds
_HEALTH_CHECK_INTERVAL = 0.5  # seconds
_MOCK_CONFIG_CONTAINER_PATH = "/home/StepFunctionsLocal/MockConfigFile.json"


class SfnLocalContainerError(Exception):
    """Raised when the Step Functions Local container encounters an error."""


class SfnLocalContainer:
    """Manages the amazon/aws-stepfunctions-local Docker container."""

    def __init__(self, mock_config_path: str, port: int = 8083) -> None:
        """Initialise container manager.

        Args:
            mock_config_path: Absolute path to the MockConfigFile.json on the host.
            port: Host port to map to container port 8083. Defaults to 8083.
        """
        self._mock_config_path = Path(mock_config_path).resolve()
        self._port = port
        self._container: Container | None = None
        self._client: docker.DockerClient | None = None

        if not self._mock_config_path.exists():
            raise FileNotFoundError(
                f"MockConfigFile.json not found: {self._mock_config_path}"
            )

    @property
    def port(self) -> int:
        """Return the configured host port."""
        return self._port

    @property
    def endpoint_url(self) -> str:
        """Return the endpoint URL for the Step Functions Local service."""
        return f"http://localhost:{self._port}"

    def start(self) -> None:
        """Start the Step Functions Local container and wait for health check.

        Pulls the image if not present, starts the container with the mock config
        mounted, and polls the health check endpoint until the service is ready
        or the timeout (30s) is exceeded.

        Raises:
            SfnLocalContainerError: If Docker is not available, container fails
                to start, or health check times out.
        """
        try:
            self._client = docker.from_env()
            self._client.ping()
        except DockerException as e:
            raise SfnLocalContainerError(
                "Docker is not available. Ensure Docker is running. "
                f"Original error: {e}"
            ) from e

        # Clean up any existing container with the same name
        self._cleanup_existing()

        container_name = f"{_CONTAINER_NAME_PREFIX}-{self._port}"

        logger.info(
            "Starting Step Functions Local container on port %d with mock config: %s",
            self._port,
            self._mock_config_path,
        )

        try:
            self._container = self._client.containers.run(
                image=_IMAGE,
                name=container_name,
                detach=True,
                ports={"8083/tcp": self._port},
                volumes={
                    str(self._mock_config_path): {
                        "bind": _MOCK_CONFIG_CONTAINER_PATH,
                        "mode": "ro",
                    }
                },
                environment={
                    "SFN_MOCK_CONFIG": _MOCK_CONFIG_CONTAINER_PATH,
                    "AWS_DEFAULT_REGION": "ap-southeast-2",
                    "AWS_ACCESS_KEY_ID": "testing",
                    "AWS_SECRET_ACCESS_KEY": "testing",  # pragma: allowlist secret
                },
                remove=False,
            )
        except DockerException as e:
            raise SfnLocalContainerError(
                f"Failed to start Step Functions Local container: {e}"
            ) from e

        # Wait for health check
        if not self._wait_for_healthy():
            # Grab container logs for debugging
            logs = self._get_container_logs()
            self.stop()
            raise SfnLocalContainerError(
                f"Step Functions Local container failed health check after "
                f"{_HEALTH_CHECK_TIMEOUT}s. Container logs:\n{logs}"
            )

        logger.info(
            "Step Functions Local container is healthy at %s", self.endpoint_url
        )

    def stop(self) -> None:
        """Stop and remove the container.

        Safe to call even if the container is not running or was never started.
        """
        if self._container is not None:
            try:
                self._container.stop(timeout=5)
                logger.info("Container stopped.")
            except (DockerException, NotFound):
                pass  # Container already stopped or removed

            try:
                self._container.remove(force=True)
                logger.info("Container removed.")
            except (DockerException, NotFound):
                pass  # Container already removed

            self._container = None

        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

    def is_healthy(self) -> bool:
        """Check if the container is accepting connections on the configured port.

        Performs a TCP connection check to localhost on the configured port.

        Returns:
            True if a TCP connection can be established, False otherwise.
        """
        return self._tcp_check()

    def _wait_for_healthy(self) -> bool:
        """Poll the health check until healthy or timeout exceeded.

        Returns:
            True if the service became healthy within the timeout, False otherwise.
        """
        deadline = time.monotonic() + _HEALTH_CHECK_TIMEOUT
        while time.monotonic() < deadline:
            if self._tcp_check():
                return True
            time.sleep(_HEALTH_CHECK_INTERVAL)
        return False

    def _tcp_check(self) -> bool:
        """Attempt a TCP connection to the service port.

        Returns:
            True if connection succeeds, False otherwise.
        """
        try:
            with socket.create_connection(
                ("localhost", self._port), timeout=1.0
            ):
                return True
        except (ConnectionRefusedError, OSError, TimeoutError):
            return False

    def _cleanup_existing(self) -> None:
        """Remove any pre-existing container with the expected name."""
        container_name = f"{_CONTAINER_NAME_PREFIX}-{self._port}"
        if self._client is None:
            return
        try:
            existing = self._client.containers.get(container_name)
            existing.stop(timeout=2)
            existing.remove(force=True)
            logger.info("Removed pre-existing container: %s", container_name)
        except NotFound:
            pass
        except DockerException as e:
            logger.warning("Error cleaning up existing container: %s", e)

    def _get_container_logs(self) -> str:
        """Retrieve container logs for diagnostics."""
        if self._container is None:
            return "(no container)"
        try:
            return self._container.logs().decode("utf-8", errors="replace")
        except Exception:
            return "(failed to retrieve logs)"

    def __enter__(self) -> "SfnLocalContainer":
        """Support usage as a context manager."""
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        """Stop container on context manager exit."""
        self.stop()
