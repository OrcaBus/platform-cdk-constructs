"""Unit tests for the placeholder resolver module."""

import json
import tempfile
from pathlib import Path

from orcabus_pipeline_test_utils.asl_validation.placeholder_resolver import (
    PLACEHOLDER_PATTERN,
    load_placeholder_map,
    resolve_placeholders,
)


class TestResolvePlaceholders:
    """Tests for the resolve_placeholders function."""

    def test_no_placeholders(self):
        """Content without placeholders should be returned unchanged."""
        content = '{"StartAt": "MyState", "States": {}}'
        result = resolve_placeholders(content)
        assert result == content

    def test_lambda_function_arn_auto_generated(self):
        """Lambda ARN placeholders should auto-generate valid ARNs."""
        content = '"FunctionName": "${__my_handler_lambda_function_arn__}"'
        result = resolve_placeholders(content)
        assert "arn:aws:lambda:ap-southeast-2:123456789012:function:my_handler" in result
        assert "${__" not in result

    def test_state_machine_arn_auto_generated(self):
        """State machine ARN placeholders should auto-generate valid ARNs."""
        content = '"StateMachineArn": "${__process_sfn_state_machine_arn__}"'
        result = resolve_placeholders(content)
        assert "arn:aws:states:ap-southeast-2:123456789012:stateMachine:process_sfn" in result

    def test_event_bus_name_auto_generated(self):
        """Event bus name placeholders should auto-generate valid ARNs."""
        content = '"EventBusName": "${__event_bus_name__}"'
        result = resolve_placeholders(content)
        assert "arn:aws:events:ap-southeast-2:123456789012:event-bus/" in result

    def test_ssm_parameter_name_auto_generated(self):
        """SSM parameter name placeholders should auto-generate paths."""
        content = '"Name": "${__default_project_id_ssm_parameter_name__}"'
        result = resolve_placeholders(content)
        assert "/test/" in result
        assert "${__" not in result

    def test_ssm_parameter_path_prefix_auto_generated(self):
        """SSM parameter path prefix placeholders should auto-generate paths."""
        content = '"Name": "${__workflow_id_to_pipeline_id_ssm_parameter_path_prefix__}"'
        result = resolve_placeholders(content)
        assert "/test/" in result
        assert "${__" not in result

    def test_detail_type_auto_generated(self):
        """Detail type placeholders should auto-generate dot-separated strings."""
        content = '"DetailType": "${__workflow_run_update_event_detail_type__}"'
        result = resolve_placeholders(content)
        assert "${__" not in result
        # Should be a dot-separated string
        assert "." in result

    def test_status_auto_generated(self):
        """Status placeholders should auto-generate uppercase status strings."""
        content = '"status": "${__draft_status__}"'
        result = resolve_placeholders(content)
        assert result == '"status": "DRAFT"'

    def test_event_status_auto_generated(self):
        """Event status placeholders should take the first meaningful word."""
        content = '"status": "${__ready_event_status__}"'
        result = resolve_placeholders(content)
        assert result == '"status": "READY"'

    def test_stack_source_auto_generated(self):
        """Stack source placeholder should resolve to a dotted source name."""
        content = '"Source": "${__stack_source__}"'
        result = resolve_placeholders(content)
        assert result == '"Source": "orcabus.test"'

    def test_workflow_name_auto_generated(self):
        """Workflow name placeholder should resolve to a workflow string."""
        content = '"workflowName": "${__workflow_name__}"'
        result = resolve_placeholders(content)
        assert result == '"workflowName": "test-workflow"'

    def test_default_payload_version_auto_generated(self):
        """Payload version placeholder should resolve to a version string."""
        content = '"version": "${__default_payload_version__}"'
        result = resolve_placeholders(content)
        assert result == '"version": "1.0.0"'

    def test_explicit_map_overrides_auto_generation(self):
        """An explicit placeholder map should override auto-generation."""
        content = '"FunctionName": "${__my_lambda_function_arn__}"'
        explicit_map = {
            "${__my_lambda_function_arn__}": "arn:aws:lambda:us-west-2:999999999999:function:custom"
        }
        result = resolve_placeholders(content, explicit_map)
        assert "arn:aws:lambda:us-west-2:999999999999:function:custom" in result

    def test_partial_map_uses_auto_generation_for_unmapped(self):
        """Unmapped placeholders should still be auto-generated when map is partial."""
        content = (
            '"FunctionName": "${__fn_a_lambda_function_arn__}", '
            '"Source": "${__stack_source__}"'
        )
        partial_map = {
            "${__fn_a_lambda_function_arn__}": "arn:aws:lambda:us-east-1:111:function:custom-a"
        }
        result = resolve_placeholders(content, partial_map)
        assert "arn:aws:lambda:us-east-1:111:function:custom-a" in result
        assert "orcabus.test" in result

    def test_multiple_placeholders_in_content(self):
        """Multiple distinct placeholders should all be resolved."""
        content = json.dumps({
            "FunctionName": "${__handler_lambda_function_arn__}",
            "EventBusName": "${__event_bus_name__}",
            "Source": "${__stack_source__}",
        })
        result = resolve_placeholders(content)
        # No unresolved placeholders should remain
        assert "${__" not in result

    def test_repeated_placeholder_resolved_consistently(self):
        """The same placeholder appearing multiple times should resolve identically."""
        content = (
            '"First": "${__my_lambda_function_arn__}", '
            '"Second": "${__my_lambda_function_arn__}"'
        )
        result = resolve_placeholders(content)
        # Extract the two resolved values
        parts = result.split('"First": "')[1].split('", "Second": "')
        assert parts[0] == parts[1].rstrip('"')

    def test_empty_map_triggers_auto_generation(self):
        """An empty dict should still trigger auto-generation (same as None)."""
        content = '"FunctionName": "${__my_lambda_function_arn__}"'
        result = resolve_placeholders(content, {})
        assert "arn:aws:lambda:" in result

    def test_generic_fallback_for_unknown_pattern(self):
        """Unknown placeholder patterns should get a hyphenated fallback value."""
        content = '"Value": "${__some_unknown_thing__}"'
        result = resolve_placeholders(content)
        assert "${__" not in result
        # Fallback converts underscores to hyphens
        assert "some-unknown-thing" in result

    def test_real_world_asl_snippet(self):
        """Test with a realistic ASL JSON snippet from OrcaBus services."""
        content = json.dumps({
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Arguments": {
                "FunctionName": "${__validate_draft_complete_schema_lambda_function_arn__}",
                "Payload": {"data": "some-data"},
            },
            "Next": "Check Result",
        })
        result = resolve_placeholders(content)
        parsed = json.loads(result)
        fn_name = parsed["Arguments"]["FunctionName"]
        assert fn_name.startswith("arn:aws:lambda:")
        assert "validate_draft_complete_schema" in fn_name


class TestLoadPlaceholderMap:
    """Tests for the load_placeholder_map function."""

    def test_load_valid_json_file(self):
        """Should load a valid JSON placeholder map file."""
        map_data = {
            "${__my_lambda_function_arn__}": "arn:aws:lambda:us-east-1:123:function:test",
            "${__event_bus_name__}": "my-bus",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(map_data, f)
            f.flush()
            result = load_placeholder_map(f.name)

        assert result == map_data

    def test_load_from_path_object(self):
        """Should accept Path objects as input."""
        map_data = {"${__key__}": "value"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(map_data, f)
            f.flush()
            result = load_placeholder_map(Path(f.name))

        assert result == map_data

    def test_file_not_found_raises(self):
        """Should raise FileNotFoundError for missing files."""
        import pytest

        with pytest.raises(FileNotFoundError):
            load_placeholder_map("/nonexistent/path/map.json")

    def test_invalid_json_raises(self):
        """Should raise JSONDecodeError for invalid JSON."""
        import pytest

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json {{{")
            f.flush()

            with pytest.raises(json.JSONDecodeError):
                load_placeholder_map(f.name)

    def test_non_object_json_raises(self):
        """Should raise ValueError if JSON root is not an object."""
        import pytest

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(["not", "an", "object"], f)
            f.flush()

            with pytest.raises(ValueError, match="JSON object"):
                load_placeholder_map(f.name)


class TestPlaceholderPattern:
    """Tests for the PLACEHOLDER_PATTERN regex."""

    def test_matches_standard_placeholder(self):
        """Should match ${__name__} format."""
        match = PLACEHOLDER_PATTERN.search("${__my_placeholder__}")
        assert match is not None
        assert match.group(1) == "my_placeholder"

    def test_does_not_match_partial(self):
        """Should not match incomplete placeholder syntax."""
        assert PLACEHOLDER_PATTERN.search("${my_placeholder}") is None
        assert PLACEHOLDER_PATTERN.search("${__my_placeholder}") is None
        assert PLACEHOLDER_PATTERN.search("__my_placeholder__") is None

    def test_matches_with_numbers(self):
        """Should match placeholders containing numbers."""
        match = PLACEHOLDER_PATTERN.search("${__v2_handler_lambda_function_arn__}")
        assert match is not None
        assert match.group(1) == "v2_handler_lambda_function_arn"

    def test_findall_multiple(self):
        """Should find all placeholders in a string."""
        content = '${__first__} middle ${__second__}'
        matches = PLACEHOLDER_PATTERN.findall(content)
        assert matches == ["first", "second"]
