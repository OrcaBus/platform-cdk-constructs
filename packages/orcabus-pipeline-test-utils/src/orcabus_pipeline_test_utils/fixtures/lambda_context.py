"""Mock Lambda context fixture.

Provides a lambda_context fixture returning a mock AWS Lambda context object
with configurable function_name, memory_limit_in_mb, and aws_request_id.
"""

import uuid
from dataclasses import dataclass, field
from typing import Callable

import pytest


@dataclass
class MockLambdaContext:
    """Mock AWS Lambda context object.

    Mimics the attributes available on the real Lambda context object
    passed to handler functions at runtime.
    """

    function_name: str = "test-function"
    memory_limit_in_mb: int = 128
    aws_request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    function_version: str = "$LATEST"
    invoked_function_arn: str = ""
    log_group_name: str = ""
    log_stream_name: str = ""

    def __post_init__(self) -> None:
        """Set derived attributes based on function_name if not explicitly provided."""
        if not self.invoked_function_arn:
            self.invoked_function_arn = (
                f"arn:aws:lambda:ap-southeast-2:123456789012:function:{self.function_name}"
            )
        if not self.log_group_name:
            self.log_group_name = f"/aws/lambda/{self.function_name}"
        if not self.log_stream_name:
            self.log_stream_name = (
                f"2024/01/01/[$LATEST]{self.aws_request_id.replace('-', '')}"
            )

    def get_remaining_time_in_millis(self) -> int:
        """Return remaining execution time in milliseconds.

        Returns a fixed value for testing purposes.
        """
        return 300000  # 5 minutes


@pytest.fixture
def lambda_context() -> Callable[..., MockLambdaContext]:
    """Factory fixture for creating mock Lambda context objects.

    Returns a factory function that creates MockLambdaContext instances.
    Call with no arguments for sensible defaults, or pass keyword arguments
    to override specific attributes.

    Usage:
        def test_handler(lambda_context):
            # With defaults
            ctx = lambda_context()

            # With custom values
            ctx = lambda_context(
                function_name="my-function",
                memory_limit_in_mb=256,
                aws_request_id="550e8400-e29b-41d4-a716-446655440000",
            )

            result = handler(event, ctx)
    """

    def _factory(
        function_name: str = "test-function",
        memory_limit_in_mb: int = 128,
        aws_request_id: str | None = None,
        function_version: str = "$LATEST",
        invoked_function_arn: str = "",
        log_group_name: str = "",
        log_stream_name: str = "",
    ) -> MockLambdaContext:
        if aws_request_id is None:
            aws_request_id = str(uuid.uuid4())

        return MockLambdaContext(
            function_name=function_name,
            memory_limit_in_mb=memory_limit_in_mb,
            aws_request_id=aws_request_id,
            function_version=function_version,
            invoked_function_arn=invoked_function_arn,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

    return _factory
