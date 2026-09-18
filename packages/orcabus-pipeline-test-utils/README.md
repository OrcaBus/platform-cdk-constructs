# orcabus-pipeline-test-utils

Shared test utilities for OrcaBus Pipeline Orchestrator services. Provides pytest fixtures,
ASL validation, a Step Functions TestState API test harness, and post-deployment smoke
test utilities.

## Installation

```bash
# From a consuming service's pyproject.toml
pip install -e "path/to/platform-cdk-constructs/packages/orcabus-pipeline-test-utils"

# Or as a git dependency
pip install "orcabus-pipeline-test-utils @ git+https://github.com/OrcaBus/platform-cdk-constructs.git#subdirectory=packages/orcabus-pipeline-test-utils"
```

Requires Python >= 3.12.

## Modules

| Module | Purpose | When it runs |
|--------|---------|--------------|
| `fixtures` | Moto-based AWS mocks, Lambda context, event builder | Pre-deployment (unit tests) |
| `asl_validation` | Structural validation of ASL JSON definitions | Pre-deployment (unit tests) |
| `sfn_teststate` | Step Functions TestState API integration tests | Pre-deployment (integration tests) |
| `smoke` | Live resource verification (Lambda, SFN, SSM) | Post-deployment (smoke tests) |

## Pytest Plugin (auto-registered fixtures)

When installed, the package registers a pytest plugin via the `pytest11` entry point. This
makes shared fixtures available to any test session automatically — no `conftest.py` imports
needed.

### Available fixtures

#### `mock_s3_client` / `mock_ssm_client` / `mock_secretsmanager_client` / `mock_events_client`

Session-scoped moto-based boto3 clients for S3, SSM, Secrets Manager, and EventBridge.
Region defaults to `ap-southeast-2`.

```python
def test_s3_upload(mock_s3_client):
    mock_s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )
    mock_s3_client.put_object(Bucket="test-bucket", Key="data.json", Body=b"{}")
    response = mock_s3_client.get_object(Bucket="test-bucket", Key="data.json")
    assert response["Body"].read() == b"{}"
```

#### `lambda_context`

Factory fixture that creates mock Lambda context objects with configurable attributes.

```python
def test_handler(lambda_context):
    ctx = lambda_context(function_name="my-function", memory_limit_in_mb=256)
    result = handler({"key": "value"}, ctx)
    assert result["statusCode"] == 200
```

#### `event_builder`

Factory fixture for building Lambda event payloads.

```python
def test_handler(event_builder, lambda_context):
    event = event_builder({"detail": {"sample_id": "SBJ00001"}})
    result = handler(event, lambda_context())
    assert result["statusCode"] == 200
```

## ASL Validation

Validates Amazon States Language JSON definitions for structural correctness without
requiring deployment or Docker.

```python
import json
from orcabus_pipeline_test_utils.asl_validation.validator import (
    validate_asl_definition,
    ValidationCategory,
)

def test_state_machine_definition_valid():
    with open("step-functions-templates/my_workflow.asl.json") as f:
        asl = json.load(f)

    result = validate_asl_definition(asl, file_path="my_workflow.asl.json")
    assert result.category == ValidationCategory.SUCCESS, result.errors
```

Checks performed:
- Required top-level fields (`StartAt`, `States`)
- Valid state types (Task, Pass, Choice, Wait, Succeed, Fail, Parallel, Map)
- `StartAt` references an existing state
- `Next` fields reference existing states
- Choice state branch targets and `Default` reference existing states
- Parallel branch and Map ItemProcessor `StartAt` validation

### Placeholder resolver

Use `placeholder_resolver` to substitute `${__xxx__}` placeholders in ASL template
strings before parsing and validation:

```python
import json
from orcabus_pipeline_test_utils.asl_validation.placeholder_resolver import resolve_placeholders

with open("step-functions-templates/my_workflow.asl.json") as f:
    raw_asl_content = f.read()

resolved_content = resolve_placeholders(raw_asl_content)
asl = json.loads(resolved_content)
result = validate_asl_definition(asl)
```

### Reference checker

Use `reference_checker` to verify that all Lambda ARN placeholders in your ASL
correspond to entries in your CDK lambda configuration map:

```python
from orcabus_pipeline_test_utils.asl_validation.reference_checker import check_lambda_arn_references

cdk_lambda_config = {
    "lambdas": {
        "my_handler": {
            "placeholder": "${__my_handler_lambda_function_arn__}",
            "entry": "app/lambdas/my_handler_py",
        },
    }
}

errors = check_lambda_arn_references(asl_definition, cdk_lambda_config)
assert errors == []
```

## Step Functions TestState API (integration tests)

Tests individual states in your Step Functions definitions using the AWS
[TestState API](https://docs.aws.amazon.com/step-functions/latest/apireference/API_TestState.html).
Supports mocked service integrations, chained state execution, and data flow assertions.

### Testing a single state

```python
from orcabus_pipeline_test_utils.sfn_teststate import TestStateClient, TestStateAssertion

client = TestStateClient(role_arn="arn:aws:iam::123456789012:role/sfn-test-role")

result = client.test_state(
    definition=asl_definition,
    input_data={"sample_id": "SBJ00001"},
    state_name="LaunchDragen",
    mock_result={"job_id": "job-123", "status": "LAUNCHED"},
)

assertion = TestStateAssertion(result)
assert assertion.assert_succeeded().passed
assert assertion.assert_output({"job_id": "{% any_string %}", "status": "LAUNCHED"}).passed
assert assertion.assert_next_state("CheckStatus").passed
```

### Chaining states (execution path)

```python
from orcabus_pipeline_test_utils.sfn_teststate import TestStateClient, PathAssertion

client = TestStateClient(role_arn="arn:aws:iam::123456789012:role/sfn-test-role")

results = client.test_path(
    definition=asl_definition,
    input_data={"sample_id": "SBJ00001"},
    state_mocks={
        "LaunchDragen": {"result": {"job_id": "job-123", "status": "LAUNCHED"}},
        "CheckStatus": {"result": {"status": "COMPLETE", "output_uri": "s3://results/"}},
    },
)

path = PathAssertion(results)
assert path.assert_path_succeeded().passed
assert path.assert_step_count(3).passed
assert path.assert_terminal_output({"status": "COMPLETE", "output_uri": "s3://results/"}).passed
```

### Data flow inspection

```python
assertion = TestStateAssertion(result)
assert assertion.assert_data_flow(
    after_input_path={"sample_id": "SBJ00001"},
    after_parameters={"FunctionName": "{% any_string %}", "Payload": {"sample_id": "SBJ00001"}},
).passed
```

## Post-Deployment Smoke Tests

Verify that deployed AWS resources are functional. These run **after** deployment and
require AWS credentials with appropriate permissions.

### Lambda DryRun check

Calls `Invoke(DryRun)` — validates permissions and configuration without executing code:

```python
import boto3
from orcabus_pipeline_test_utils.smoke.lambda_check import check_lambda_invocable

session = boto3.Session()
result = check_lambda_invocable("my-function-name", session)
assert result.passed, f"{result.error_type}: {result.error_message}"
```

### State Machine check

Calls `DescribeStateMachine` and verifies status is ACTIVE with a non-null definition:

```python
from orcabus_pipeline_test_utils.smoke.sfn_check import check_state_machine_active

result = check_state_machine_active(
    "arn:aws:states:ap-southeast-2:123456789012:stateMachine:MyWorkflow",
    session,
)
assert result.passed, f"{result.error_type}: {result.error_message}"
```

### SSM Parameter check

Verifies SSM parameters exist and are readable:

```python
from orcabus_pipeline_test_utils.smoke.ssm_check import check_ssm_parameters_exist

results = check_ssm_parameters_exist(
    ["/orcabus/config/api-url", "/orcabus/config/event-bus-name"],
    session,
)
for r in results:
    assert r.passed, f"{r.resource_name}: {r.error_message}"
```

### SmokeTestResult

All smoke checks return `SmokeTestResult`:

```python
@dataclass
class SmokeTestResult:
    resource_name: str
    resource_type: str         # "lambda" | "state_machine" | "ssm_parameter"
    passed: bool
    error_type: str | None     # "auth" | "config" | None
    error_message: str | None
```

Error classification:
- `auth` — IAM/credential issues (AccessDeniedException, ExpiredTokenException)
- `config` — Resource doesn't exist or is misconfigured

## Pipeline Integration

### Pre-deployment tests (unitAppTestConfig)

ASL validation and TestState API tests run in the pipeline's `unitAppTestConfig` CodeBuild
step, which executes before CDK synth.

```typescript
unitAppTestConfig: {
  installCommands: [
    ...DEFAULT_INSTALL_COMMANDS,
    'pip install -e "./app[test]"',
  ],
  command: [
    'pytest app/step-functions-templates/tests/ -v --tb=short',
  ],
  partialBuildSpec: {
    phases: { install: { 'runtime-versions': { nodejs: '22.x', python: '3.14' } } },
    version: '0.2',
  },
}
```

### Post-deployment tests (pipeline stage `post` step)

Smoke tests run after a stage deploys. They require cross-account IAM permissions and
cannot use `unitIacTestConfig` or `unitAppTestConfig` (those run before any deployment).

```typescript
// Add as a post-deployment step on a stage
cdkPipeline.addStage(betaStage, {
  post: [
    new CodeBuildStep('SmokeTestBeta', {
      commands: [
        'pip install orcabus-pipeline-test-utils',
        'pytest tests/smoke/ -v --tb=short',
      ],
      rolePolicyStatements: [
        new PolicyStatement({
          actions: ['lambda:InvokeFunction'],
          resources: ['arn:aws:lambda:ap-southeast-2:*:function:my-service-*'],
        }),
        new PolicyStatement({
          actions: ['states:DescribeStateMachine'],
          resources: ['*'],
        }),
        new PolicyStatement({
          actions: ['ssm:GetParameter'],
          resources: ['arn:aws:ssm:ap-southeast-2:*:parameter/orcabus/*'],
        }),
      ],
    }),
  ],
});
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run the package's own tests
pytest tests/ -v
```
