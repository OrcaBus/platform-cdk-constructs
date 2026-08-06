"""Unit tests for the SFN Local CLI runner entry point."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from orcabus_pipeline_test_utils.sfn_local.runner import (
    TimeoutExpiredError,
    _resolve_mock_config_path,
    parse_args,
    run,
    _run_pytest,
    _DEFAULT_TIMEOUT,
    _DEFAULT_PORT,
)


class TestParseArgs:
    """Test argument parsing."""

    def test_required_args(self) -> None:
        args = parse_args(["--mock-config", "/path/to/mocks", "--tests", "/path/to/tests"])
        assert args.mock_config == "/path/to/mocks"
        assert args.tests == "/path/to/tests"
        assert args.timeout == _DEFAULT_TIMEOUT
        assert args.port == _DEFAULT_PORT

    def test_custom_timeout(self) -> None:
        args = parse_args([
            "--mock-config", "/path/to/mocks",
            "--tests", "/path/to/tests",
            "--timeout", "60",
        ])
        assert args.timeout == 60

    def test_custom_port(self) -> None:
        args = parse_args([
            "--mock-config", "/path/to/mocks",
            "--tests", "/path/to/tests",
            "--port", "9090",
        ])
        assert args.port == 9090

    def test_missing_required_args_raises(self) -> None:
        with pytest.raises(SystemExit):
            parse_args([])

    def test_missing_tests_arg_raises(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["--mock-config", "/path/to/mocks"])

    def test_missing_mock_config_arg_raises(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["--tests", "/path/to/tests"])


class TestResolveMockConfigPath:
    """Test mock config path resolution."""

    def test_resolves_direct_file_path(self, tmp_path: Path) -> None:
        config_file = tmp_path / "MockConfigFile.json"
        config_file.write_text("{}")
        result = _resolve_mock_config_path(str(config_file))
        assert result == config_file.resolve()

    def test_resolves_directory_with_mock_config(self, tmp_path: Path) -> None:
        config_file = tmp_path / "MockConfigFile.json"
        config_file.write_text("{}")
        result = _resolve_mock_config_path(str(tmp_path))
        assert result == config_file.resolve()

    def test_raises_for_directory_without_mock_config(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="MockConfigFile.json not found"):
            _resolve_mock_config_path(str(tmp_path))

    def test_raises_for_nonexistent_path(self, tmp_path: Path) -> None:
        nonexistent = tmp_path / "nonexistent"
        with pytest.raises(FileNotFoundError, match="does not exist"):
            _resolve_mock_config_path(str(nonexistent))


class TestRun:
    """Test the main run() orchestration function."""

    @pytest.fixture
    def mock_config_dir(self, tmp_path: Path) -> Path:
        """Create a temp directory with a MockConfigFile.json."""
        config_file = tmp_path / "mocks" / "MockConfigFile.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text('{"StateMachines": {}, "MockedResponses": {}}')
        return config_file.parent

    @pytest.fixture
    def tests_dir(self, tmp_path: Path) -> Path:
        """Create a temp tests directory."""
        tests = tmp_path / "tests"
        tests.mkdir()
        (tests / "test_example.py").write_text("def test_pass(): pass")
        return tests

    def test_returns_1_when_mock_config_not_found(self, tmp_path: Path) -> None:
        exit_code = run([
            "--mock-config", str(tmp_path / "nonexistent"),
            "--tests", str(tmp_path),
        ])
        assert exit_code == 1

    def test_returns_1_when_tests_path_not_found(
        self, mock_config_dir: Path, tmp_path: Path
    ) -> None:
        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tmp_path / "nonexistent_tests"),
        ])
        assert exit_code == 1

    def test_returns_1_when_timeout_invalid(
        self, mock_config_dir: Path, tests_dir: Path
    ) -> None:
        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tests_dir),
            "--timeout", "0",
        ])
        assert exit_code == 1

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.SfnLocalContainer")
    @patch("orcabus_pipeline_test_utils.sfn_local.runner._run_pytest")
    def test_successful_run_returns_pytest_exit_code(
        self,
        mock_run_pytest: MagicMock,
        mock_container_cls: MagicMock,
        mock_config_dir: Path,
        tests_dir: Path,
    ) -> None:
        mock_container = MagicMock()
        mock_container.endpoint_url = "http://localhost:8083"
        mock_container_cls.return_value = mock_container
        mock_run_pytest.return_value = 0

        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tests_dir),
        ])

        assert exit_code == 0
        mock_container.start.assert_called_once()
        mock_container.stop.assert_called_once()
        mock_run_pytest.assert_called_once()

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.SfnLocalContainer")
    @patch("orcabus_pipeline_test_utils.sfn_local.runner._run_pytest")
    def test_failed_tests_return_nonzero(
        self,
        mock_run_pytest: MagicMock,
        mock_container_cls: MagicMock,
        mock_config_dir: Path,
        tests_dir: Path,
    ) -> None:
        mock_container = MagicMock()
        mock_container.endpoint_url = "http://localhost:8083"
        mock_container_cls.return_value = mock_container
        mock_run_pytest.return_value = 1

        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tests_dir),
        ])

        assert exit_code == 1
        mock_container.stop.assert_called_once()

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.SfnLocalContainer")
    def test_container_error_returns_1(
        self,
        mock_container_cls: MagicMock,
        mock_config_dir: Path,
        tests_dir: Path,
    ) -> None:
        from orcabus_pipeline_test_utils.sfn_local.container import (
            SfnLocalContainerError,
        )

        mock_container = MagicMock()
        mock_container.start.side_effect = SfnLocalContainerError("Docker unavailable")
        mock_container_cls.return_value = mock_container

        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tests_dir),
        ])

        assert exit_code == 1
        mock_container.stop.assert_called_once()

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.SfnLocalContainer")
    @patch("orcabus_pipeline_test_utils.sfn_local.runner._run_pytest")
    def test_timeout_expired_returns_1(
        self,
        mock_run_pytest: MagicMock,
        mock_container_cls: MagicMock,
        mock_config_dir: Path,
        tests_dir: Path,
    ) -> None:
        mock_container = MagicMock()
        mock_container.endpoint_url = "http://localhost:8083"
        mock_container_cls.return_value = mock_container
        mock_run_pytest.side_effect = TimeoutExpiredError("Exceeded budget")

        exit_code = run([
            "--mock-config", str(mock_config_dir),
            "--tests", str(tests_dir),
        ])

        assert exit_code == 1
        mock_container.stop.assert_called_once()

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.SfnLocalContainer")
    @patch("orcabus_pipeline_test_utils.sfn_local.runner._run_pytest")
    def test_container_always_stopped_even_on_error(
        self,
        mock_run_pytest: MagicMock,
        mock_container_cls: MagicMock,
        mock_config_dir: Path,
        tests_dir: Path,
    ) -> None:
        mock_container = MagicMock()
        mock_container.endpoint_url = "http://localhost:8083"
        mock_container_cls.return_value = mock_container
        mock_run_pytest.side_effect = RuntimeError("Unexpected error")

        # Even unexpected errors should stop the container
        with pytest.raises(RuntimeError):
            run([
                "--mock-config", str(mock_config_dir),
                "--tests", str(tests_dir),
            ])

        mock_container.stop.assert_called_once()


class TestRunPytest:
    """Test the _run_pytest subprocess execution."""

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.subprocess.run")
    def test_passes_correct_command(
        self, mock_subprocess_run: MagicMock, tmp_path: Path
    ) -> None:
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        tests_path = tmp_path / "tests"
        tests_path.mkdir()

        result = _run_pytest(
            tests_path=tests_path,
            endpoint_url="http://localhost:8083",
            timeout=60.0,
        )

        assert result == 0
        call_args = mock_subprocess_run.call_args
        cmd = call_args[0][0]
        assert sys.executable in cmd[0]
        assert "-m" in cmd
        assert "pytest" in cmd
        assert str(tests_path) in cmd
        assert "-v" in cmd
        assert "--tb=short" in cmd
        assert "sfn_local" in cmd

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.subprocess.run")
    def test_sets_endpoint_url_env_var(
        self, mock_subprocess_run: MagicMock, tmp_path: Path
    ) -> None:
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        tests_path = tmp_path / "tests"
        tests_path.mkdir()

        _run_pytest(
            tests_path=tests_path,
            endpoint_url="http://localhost:9090",
            timeout=60.0,
        )

        call_kwargs = mock_subprocess_run.call_args[1]
        assert call_kwargs["env"]["SFN_LOCAL_ENDPOINT_URL"] == "http://localhost:9090"

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.subprocess.run")
    def test_raises_timeout_expired_error(
        self, mock_subprocess_run: MagicMock, tmp_path: Path
    ) -> None:
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd="pytest", timeout=60
        )
        tests_path = tmp_path / "tests"
        tests_path.mkdir()

        with pytest.raises(TimeoutExpiredError):
            _run_pytest(
                tests_path=tests_path,
                endpoint_url="http://localhost:8083",
                timeout=60.0,
            )

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.subprocess.run")
    def test_returns_nonzero_exit_code_on_test_failure(
        self, mock_subprocess_run: MagicMock, tmp_path: Path
    ) -> None:
        mock_subprocess_run.return_value = MagicMock(returncode=1)
        tests_path = tmp_path / "tests"
        tests_path.mkdir()

        result = _run_pytest(
            tests_path=tests_path,
            endpoint_url="http://localhost:8083",
            timeout=60.0,
        )

        assert result == 1

    @patch("orcabus_pipeline_test_utils.sfn_local.runner.subprocess.run")
    def test_respects_timeout_parameter(
        self, mock_subprocess_run: MagicMock, tmp_path: Path
    ) -> None:
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        tests_path = tmp_path / "tests"
        tests_path.mkdir()

        _run_pytest(
            tests_path=tests_path,
            endpoint_url="http://localhost:8083",
            timeout=120.0,
        )

        call_kwargs = mock_subprocess_run.call_args[1]
        assert call_kwargs["timeout"] == 120.0
