"""Unit tests for the lambda_context fixture."""

import uuid

from orcabus_pipeline_test_utils.fixtures.lambda_context import MockLambdaContext


class TestMockLambdaContext:
    """Tests for MockLambdaContext dataclass."""

    def test_default_values(self):
        """MockLambdaContext should have sensible defaults."""
        ctx = MockLambdaContext()
        assert ctx.function_name == "test-function"
        assert ctx.memory_limit_in_mb == 128
        # aws_request_id should be a valid UUID
        uuid.UUID(ctx.aws_request_id)
        assert ctx.function_version == "$LATEST"

    def test_custom_values(self):
        """MockLambdaContext should accept custom attribute values."""
        request_id = str(uuid.uuid4())
        ctx = MockLambdaContext(
            function_name="my-function",
            memory_limit_in_mb=256,
            aws_request_id=request_id,
        )
        assert ctx.function_name == "my-function"
        assert ctx.memory_limit_in_mb == 256
        assert ctx.aws_request_id == request_id

    def test_derived_attributes(self):
        """MockLambdaContext should derive ARN and log attributes from function_name."""
        ctx = MockLambdaContext(function_name="my-func")
        assert ctx.invoked_function_arn == (
            "arn:aws:lambda:ap-southeast-2:123456789012:function:my-func"
        )
        assert ctx.log_group_name == "/aws/lambda/my-func"
        assert "$LATEST" in ctx.log_stream_name

    def test_explicit_arn_not_overridden(self):
        """When invoked_function_arn is explicitly set, it should not be overridden."""
        custom_arn = "arn:aws:lambda:us-east-1:999999999999:function:custom"
        ctx = MockLambdaContext(
            function_name="my-func",
            invoked_function_arn=custom_arn,
        )
        assert ctx.invoked_function_arn == custom_arn

    def test_get_remaining_time_in_millis(self):
        """get_remaining_time_in_millis should return a positive integer."""
        ctx = MockLambdaContext()
        remaining = ctx.get_remaining_time_in_millis()
        assert isinstance(remaining, int)
        assert remaining > 0


class TestLambdaContextFixture:
    """Tests for the lambda_context factory fixture."""

    def test_factory_returns_context_with_defaults(self, lambda_context):
        """Factory with no args should return context with default values."""
        ctx = lambda_context()
        assert ctx.function_name == "test-function"
        assert ctx.memory_limit_in_mb == 128
        uuid.UUID(ctx.aws_request_id)  # Should be valid UUID

    def test_factory_accepts_custom_function_name(self, lambda_context):
        """Factory should allow overriding function_name."""
        ctx = lambda_context(function_name="custom-handler")
        assert ctx.function_name == "custom-handler"

    def test_factory_accepts_custom_memory(self, lambda_context):
        """Factory should allow overriding memory_limit_in_mb."""
        ctx = lambda_context(memory_limit_in_mb=512)
        assert ctx.memory_limit_in_mb == 512

    def test_factory_accepts_custom_request_id(self, lambda_context):
        """Factory should allow overriding aws_request_id."""
        request_id = "550e8400-e29b-41d4-a716-446655440000"
        ctx = lambda_context(aws_request_id=request_id)
        assert ctx.aws_request_id == request_id

    def test_factory_generates_unique_request_ids(self, lambda_context):
        """Each call without explicit request_id should generate a unique UUID."""
        ctx1 = lambda_context()
        ctx2 = lambda_context()
        assert ctx1.aws_request_id != ctx2.aws_request_id

    def test_factory_all_custom_values(self, lambda_context):
        """Factory should accept all custom values simultaneously."""
        request_id = str(uuid.uuid4())
        ctx = lambda_context(
            function_name="full-custom",
            memory_limit_in_mb=1024,
            aws_request_id=request_id,
        )
        assert ctx.function_name == "full-custom"
        assert ctx.memory_limit_in_mb == 1024
        assert ctx.aws_request_id == request_id
