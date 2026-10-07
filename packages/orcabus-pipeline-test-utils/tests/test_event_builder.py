"""Tests for the event_builder fixture."""


def test_event_builder_returns_callable(event_builder):
    """The fixture should return a callable factory function."""
    assert callable(event_builder)


def test_event_builder_passthrough_simple_dict(event_builder):
    """The factory should return the same dict that was passed in."""
    payload = {"key": "value"}
    result = event_builder(payload)
    assert result == {"key": "value"}


def test_event_builder_passthrough_nested_dict(event_builder):
    """The factory should handle nested dictionaries."""
    payload = {"data": {"nested": True, "items": [1, 2, 3]}}
    result = event_builder(payload)
    assert result == {"data": {"nested": True, "items": [1, 2, 3]}}


def test_event_builder_passthrough_empty_dict(event_builder):
    """The factory should handle an empty dictionary."""
    payload: dict = {}
    result = event_builder(payload)
    assert result == {}


def test_event_builder_returns_same_reference(event_builder):
    """The factory should return the exact same dict object (not a copy)."""
    payload = {"key": "value"}
    result = event_builder(payload)
    assert result is payload


def test_event_builder_complex_event_payload(event_builder):
    """The factory should handle a realistic Lambda event payload."""
    payload = {
        "version": "0",
        "source": "orcabus.dragenwgtsdna",
        "detail-type": "WorkflowRunStateChange",
        "detail": {
            "status": "DRAFT",
            "workflowName": "dragen-wgts-dna",
            "payload": {
                "version": "2025.08.05",
                "data": {
                    "libraryId": "LIB001",
                    "sampleId": "SMP001",
                },
            },
        },
    }
    result = event_builder(payload)
    assert result == payload
    assert result["detail"]["status"] == "DRAFT"
