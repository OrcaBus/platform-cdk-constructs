"""Unit tests for MockConfigBuilder."""

import json
import os
import tempfile

import pytest

from orcabus_pipeline_test_utils.sfn_local.mock_config import MockConfigBuilder


class TestAddStateMachine:
    """Tests for add_state_machine."""

    def test_add_single_state_machine(self):
        """Adding a state machine includes it in the build output."""
        builder = MockConfigBuilder()
        result = builder.add_state_machine("MyStateMachine")

        assert result is builder  # fluent return
        output = builder.build()
        assert "MyStateMachine" in output["StateMachines"]
        assert output["StateMachines"]["MyStateMachine"] == {"TestCases": {}}

    def test_add_multiple_state_machines(self):
        """Adding multiple state machines includes all in output."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1").add_state_machine("SM2")

        output = builder.build()
        assert "SM1" in output["StateMachines"]
        assert "SM2" in output["StateMachines"]

    def test_add_duplicate_state_machine_is_idempotent(self):
        """Adding the same state machine twice doesn't create duplicates."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1").add_state_machine("SM1")

        output = builder.build()
        assert len(output["StateMachines"]) == 1

    def test_add_empty_name_raises(self):
        """Adding a state machine with empty name raises ValueError."""
        builder = MockConfigBuilder()
        with pytest.raises(ValueError, match="must not be empty"):
            builder.add_state_machine("")


class TestAddTestCase:
    """Tests for add_test_case."""

    def test_add_test_case_to_existing_machine(self):
        """Adding a test case to a registered state machine works."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1")
        result = builder.add_test_case(
            "SM1", "HappyPath", {"InvokeLambda": "MockLambdaResponse"}
        )

        assert result is builder
        output = builder.build()
        test_cases = output["StateMachines"]["SM1"]["TestCases"]
        assert "HappyPath" in test_cases
        assert test_cases["HappyPath"] == {"InvokeLambda": "MockLambdaResponse"}

    def test_add_multiple_test_cases(self):
        """Adding multiple test cases to a state machine includes all."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1")
        builder.add_test_case("SM1", "HappyPath", {"Task1": "Mock1"})
        builder.add_test_case("SM1", "ErrorPath", {"Task1": "MockError"})

        output = builder.build()
        test_cases = output["StateMachines"]["SM1"]["TestCases"]
        assert "HappyPath" in test_cases
        assert "ErrorPath" in test_cases

    def test_add_test_case_to_nonexistent_machine_raises(self):
        """Adding a test case to an unregistered state machine raises ValueError."""
        builder = MockConfigBuilder()
        with pytest.raises(ValueError, match="not found"):
            builder.add_test_case("NonExistent", "Test1", {"Task": "Mock"})

    def test_add_test_case_with_empty_name_raises(self):
        """Adding a test case with empty name raises ValueError."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1")
        with pytest.raises(ValueError, match="must not be empty"):
            builder.add_test_case("SM1", "", {"Task": "Mock"})

    def test_add_test_case_with_multiple_state_mocks(self):
        """A test case can map multiple task states to mocked responses."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM1")
        builder.add_test_case(
            "SM1",
            "FullPath",
            {
                "InvokeLambdaA": "MockResponseA",
                "InvokeLambdaB": "MockResponseB",
                "PutEvents": "MockEventResponse",
            },
        )

        output = builder.build()
        tc = output["StateMachines"]["SM1"]["TestCases"]["FullPath"]
        assert tc == {
            "InvokeLambdaA": "MockResponseA",
            "InvokeLambdaB": "MockResponseB",
            "PutEvents": "MockEventResponse",
        }


class TestAddMockedResponse:
    """Tests for add_mocked_response."""

    def test_add_return_response(self):
        """Adding a Return mocked response works correctly."""
        builder = MockConfigBuilder()
        result = builder.add_mocked_response(
            "MockLambdaResponse",
            {"0": {"Return": {"statusCode": 200, "body": "ok"}}},
        )

        assert result is builder
        output = builder.build()
        assert "MockLambdaResponse" in output["MockedResponses"]
        assert output["MockedResponses"]["MockLambdaResponse"]["0"]["Return"] == {
            "statusCode": 200,
            "body": "ok",
        }

    def test_add_throw_response(self):
        """Adding a Throw mocked response works correctly."""
        builder = MockConfigBuilder()
        builder.add_mocked_response(
            "MockErrorResponse",
            {
                "0": {
                    "Throw": {
                        "Error": "Lambda.ServiceException",
                        "Cause": "Service unavailable",
                    }
                }
            },
        )

        output = builder.build()
        resp = output["MockedResponses"]["MockErrorResponse"]["0"]
        assert resp["Throw"]["Error"] == "Lambda.ServiceException"
        assert resp["Throw"]["Cause"] == "Service unavailable"

    def test_add_multi_invocation_response(self):
        """A mocked response can have multiple invocation indices."""
        builder = MockConfigBuilder()
        builder.add_mocked_response(
            "MultiResponse",
            {
                "0": {"Return": {"attempt": 1}},
                "1": {"Return": {"attempt": 2}},
                "2": {"Throw": {"Error": "TooManyRetries", "Cause": "Exhausted"}},
            },
        )

        output = builder.build()
        resp = output["MockedResponses"]["MultiResponse"]
        assert "0" in resp
        assert "1" in resp
        assert "2" in resp
        assert resp["0"]["Return"] == {"attempt": 1}
        assert resp["2"]["Throw"]["Error"] == "TooManyRetries"

    def test_add_response_with_empty_name_raises(self):
        """Adding a response with empty name raises ValueError."""
        builder = MockConfigBuilder()
        with pytest.raises(ValueError, match="must not be empty"):
            builder.add_mocked_response("", {"0": {"Return": {}}})

    def test_add_response_without_return_or_throw_raises(self):
        """Adding a response without Return or Throw raises ValueError."""
        builder = MockConfigBuilder()
        with pytest.raises(ValueError, match="'Return' or 'Throw'"):
            builder.add_mocked_response("Bad", {"0": {"SomethingElse": {}}})


class TestBuild:
    """Tests for build()."""

    def test_empty_builder_produces_valid_structure(self):
        """An empty builder produces valid top-level keys."""
        builder = MockConfigBuilder()
        output = builder.build()

        assert "StateMachines" in output
        assert "MockedResponses" in output
        assert output["StateMachines"] == {}
        assert output["MockedResponses"] == {}

    def test_full_build_example(self):
        """A complete build produces the expected MockConfigFile structure."""
        builder = MockConfigBuilder()
        builder.add_state_machine("PopulateDraftSfn")
        builder.add_test_case(
            "PopulateDraftSfn",
            "HappyPath",
            {
                "GetWorkflowParams": "MockGetParams",
                "TransformData": "MockTransform",
            },
        )
        builder.add_test_case(
            "PopulateDraftSfn",
            "ErrorPath",
            {"GetWorkflowParams": "MockGetParamsError"},
        )
        builder.add_mocked_response(
            "MockGetParams",
            {"0": {"Return": {"workflow_id": "wfl.123"}}},
        )
        builder.add_mocked_response(
            "MockTransform",
            {"0": {"Return": {"status": "transformed"}}},
        )
        builder.add_mocked_response(
            "MockGetParamsError",
            {"0": {"Throw": {"Error": "ParameterNotFound", "Cause": "Missing param"}}},
        )

        output = builder.build()

        # Verify structure
        assert output["StateMachines"]["PopulateDraftSfn"]["TestCases"]["HappyPath"] == {
            "GetWorkflowParams": "MockGetParams",
            "TransformData": "MockTransform",
        }
        assert output["StateMachines"]["PopulateDraftSfn"]["TestCases"]["ErrorPath"] == {
            "GetWorkflowParams": "MockGetParamsError",
        }
        assert output["MockedResponses"]["MockGetParams"]["0"]["Return"] == {
            "workflow_id": "wfl.123"
        }
        assert output["MockedResponses"]["MockGetParamsError"]["0"]["Throw"] == {
            "Error": "ParameterNotFound",
            "Cause": "Missing param",
        }

    def test_build_is_serializable_to_json(self):
        """The build output is valid JSON-serializable."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM")
        builder.add_test_case("SM", "TC", {"Task": "Resp"})
        builder.add_mocked_response("Resp", {"0": {"Return": {"key": "value"}}})

        output = builder.build()
        # Should not raise
        json_str = json.dumps(output)
        parsed = json.loads(json_str)
        assert parsed == output


class TestWrite:
    """Tests for write()."""

    def test_write_creates_file(self):
        """write() creates the file with correct JSON content."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM")
        builder.add_test_case("SM", "TC", {"Task": "Mock"})
        builder.add_mocked_response("Mock", {"0": {"Return": {"ok": True}}})

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "MockConfigFile.json")
            builder.write(path)

            assert os.path.exists(path)
            with open(path) as f:
                content = json.load(f)

            assert content == builder.build()

    def test_write_creates_parent_directories(self):
        """write() creates parent directories if they don't exist."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "nested", "deep", "MockConfigFile.json")
            builder.write(path)

            assert os.path.exists(path)

    def test_write_produces_indented_json(self):
        """write() produces human-readable indented JSON."""
        builder = MockConfigBuilder()
        builder.add_state_machine("SM")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "MockConfigFile.json")
            builder.write(path)

            with open(path) as f:
                raw = f.read()

            # Should be indented (multi-line)
            assert "\n" in raw
            # Should end with newline
            assert raw.endswith("\n")


class TestFluentChaining:
    """Tests for fluent API chaining."""

    def test_full_chain(self):
        """All methods can be chained in a single expression."""
        output = (
            MockConfigBuilder()
            .add_state_machine("SM")
            .add_test_case("SM", "TC1", {"Task": "Resp1"})
            .add_test_case("SM", "TC2", {"Task": "Resp2"})
            .add_mocked_response("Resp1", {"0": {"Return": {"v": 1}}})
            .add_mocked_response("Resp2", {"0": {"Return": {"v": 2}}})
            .build()
        )

        assert len(output["StateMachines"]["SM"]["TestCases"]) == 2
        assert len(output["MockedResponses"]) == 2
