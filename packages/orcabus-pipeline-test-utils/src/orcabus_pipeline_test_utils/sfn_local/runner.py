"""CLI runner for Step Functions Local integration tests.

Orchestrates the full test lifecycle:
1. Start the Step Functions Local Docker container
2. Wait for health check
3. Run pytest against the SFN test files
4. Stop the container
5. Return the pytest exit code

Usage:
    python3.14 -m orcabus_pipeline_test_utils.sfn_local.runner \
        --mock-config app/step-functions-templates/tests/mocks/ \
        --tests app/step-functions-templates/tests/ \
        --timeout 180
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from orcabus_pipeline_test_utils.sfn_local.container import (
    SfnLocalContainer,
    SfnLocalContainerError,
)

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 180  # 3 minutes
_DEFAULT_PORT = 8083


class TimeoutExpiredError(Exception):
    """Raised when the total test budget is exceeded."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list to parse. Defaults to sys.argv[1:].

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="sfn-local-runner",
        description="Run Step Functions Local integration tests with Docker.",
    )
    parser.add_argument(
        "--mock-config",
        required=True,
        help="Path to MockConfigFile.json or directory containing it.",
    )
    parser.add_argument(
        "--tests",
        required=True,
        help="Path to the test directory or file to run with pytest.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=_DEFAULT_TIMEOUT,
        help=f"Total timeout budget in seconds (default: {_DEFAULT_TIMEOUT}).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=_DEFAULT_PORT,
        help=f"Host port for Step Functions Local (default: {_DEFAULT_PORT}).",
    )
    return parser.parse_args(argv)


def _resolve_mock_config_path(mock_config: str) -> Path:
    """Resolve the mock config path to a MockConfigFile.json file.

    If the path is a directory, look for MockConfigFile.json inside it.
    If the path is a file, use it directly.

    Args:
        mock_config: Path string from CLI arguments.

    Returns:
        Resolved absolute path to the MockConfigFile.json.

    Raises:
        FileNotFoundError: If the mock config file cannot be found.
    """
    path = Path(mock_config).resolve()

    if path.is_file():
        return path

    if path.is_dir():
        config_file = path / "MockConfigFile.json"
        if config_file.exists():
            return config_file
        raise FileNotFoundError(
            f"MockConfigFile.json not found in directory: {path}"
        )

    raise FileNotFoundError(f"Mock config path does not exist: {path}")


def run(argv: list[str] | None = None) -> int:
    """Execute the Step Functions Local test runner.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].

    Returns:
        Exit code: 0 on success, non-zero on failure.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    args = parse_args(argv)

    # Resolve mock config path
    try:
        mock_config_path = _resolve_mock_config_path(args.mock_config)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    # Validate test path exists
    tests_path = Path(args.tests).resolve()
    if not tests_path.exists():
        logger.error("Test path does not exist: %s", tests_path)
        return 1

    timeout = args.timeout
    if timeout <= 0:
        logger.error("Timeout must be a positive integer, got: %d", timeout)
        return 1

    port = args.port
    container = SfnLocalContainer(str(mock_config_path), port=port)
    start_time = time.monotonic()

    try:
        # Start container
        logger.info("Starting Step Functions Local container...")
        container.start()
        logger.info("Container started successfully at %s", container.endpoint_url)

        # Calculate remaining time for pytest
        elapsed = time.monotonic() - start_time
        remaining = timeout - elapsed
        if remaining <= 0:
            logger.error(
                "Timeout budget exhausted during container startup (%.1fs elapsed)",
                elapsed,
            )
            return 1

        # Run pytest with remaining timeout
        logger.info(
            "Running pytest on %s (timeout: %.0fs remaining)...",
            tests_path,
            remaining,
        )
        exit_code = _run_pytest(
            tests_path=tests_path,
            endpoint_url=container.endpoint_url,
            timeout=remaining,
        )

        return exit_code

    except SfnLocalContainerError as e:
        logger.error("Container error: %s", e)
        return 1
    except TimeoutExpiredError:
        logger.error(
            "Total test time exceeded %d-second budget. "
            "Killing remaining tests.",
            timeout,
        )
        return 1
    finally:
        # Always stop the container
        logger.info("Stopping Step Functions Local container...")
        container.stop()
        logger.info("Container stopped.")


def _run_pytest(
    tests_path: Path,
    endpoint_url: str,
    timeout: float,
) -> int:
    """Run pytest as a subprocess with timeout enforcement.

    Args:
        tests_path: Path to tests directory or file.
        endpoint_url: The SFN Local endpoint URL for test configuration.
        timeout: Maximum seconds to allow pytest to run.

    Returns:
        pytest exit code.

    Raises:
        TimeoutExpiredError: If pytest exceeds the timeout budget.
    """
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(tests_path),
        "-v",
        "--tb=short",
        "-m",
        "sfn_local",
    ]

    # Pass the endpoint URL as an environment variable for tests to pick up
    env = os.environ.copy()
    env["SFN_LOCAL_ENDPOINT_URL"] = endpoint_url

    try:
        result = subprocess.run(
            cmd,
            timeout=timeout,
            env=env,
            cwd=str(tests_path.parent) if tests_path.is_file() else None,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        raise TimeoutExpiredError(
            f"pytest exceeded timeout of {timeout:.0f}s"
        )
