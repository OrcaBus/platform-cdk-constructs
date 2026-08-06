"""Step Functions Local test harness.

Provides:
- container: Docker container lifecycle management
- client: boto3 client wrapper for localhost:8083
- mock_config: MockConfigFile builder/loader
- runner: CLI entry point for test execution
- assertions: Execution result assertion utilities
"""
