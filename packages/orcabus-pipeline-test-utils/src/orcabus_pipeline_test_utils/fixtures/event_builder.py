"""Event builder fixture.

Provides an event_builder fixture that accepts a dictionary payload and returns
it as the event argument for Lambda handler invocation.

Usage in tests::

    def test_my_handler(event_builder, lambda_context):
        event = event_builder({"key": "value", "data": {"nested": True}})
        result = handler(event, lambda_context)
        assert result["statusCode"] == 200
"""

from typing import Any, Callable

import pytest


@pytest.fixture
def event_builder() -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Return a factory function that builds Lambda event payloads.

    The factory accepts a dictionary payload and returns it directly as the
    event argument suitable for passing to a Lambda handler. This provides a
    clean abstraction point for future enhancements such as adding default
    wrapper structures or EventBridge envelope formatting.

    Returns:
        A callable that accepts a dict and returns it as the event payload.
    """

    def _build_event(payload: dict[str, Any]) -> dict[str, Any]:
        return payload

    return _build_event
