# Project Structure

## Top-Level Layout

```
platform-cdk-constructs/
├── packages/           # Publishable npm package (JSII-compiled CDK constructs)
├── dev/                # Development CDK app for testing constructs locally
├── .github/workflows/  # CI/CD (PR tests + npm release)
└── .kiro/steering/     # AI assistant steering rules
```

## packages/ — Construct Library

The main deliverable. Published as `@orcabus/platform-cdk-constructs`.

```
packages/
├── index.ts                        # Entry point — exports all namespaces
├── package.json                    # JSII config, dependencies, scripts
├── tsconfig.json                   # TypeScript compiler options
├── jest.config.js                  # Test configuration
│
├── api-gateway/                    # HTTP API Gateway + Cognito auth
├── deployment-stack-pipeline/      # CodePipeline (Beta→Gamma→Prod)
├── lambda/                         # PythonUvFunction + Python layers
│   ├── build_python/               # Docker build context for UV bundling
│   └── layers/                     # Lambda layer source (Poetry projects)
│       ├── orcabus_api_tools/      # OrcaBus API client/models
│       ├── mart_tools/             # Athena data mart queries
│       ├── icav2_tools/            # Illumina Connected Analytics v2
│       └── fastapi_tools/          # FastAPI + Mangum adapter
├── dynamodb/                       # DynamoDB table helpers
├── ecs/                            # ECS/Fargate constructs
├── monitored-queue/                # SQS + DLQ + CloudWatch alarms
├── named-lambda-role/              # Named IAM roles for Lambda
├── provider-function/              # Custom resource provider framework
├── eventbridge-rules/              # EventBridge + SFN Slack notifications
├── shared-config/                  # Cross-cutting constants & config
├── utils/                          # Helper functions (stage resolution, etc.)
├── orcabus-pipeline-test-utils/    # Python pytest utilities
├── test/                           # CDK unit/snapshot tests
├── docs/                           # Auto-generated typedoc markdown
└── dist/                           # JSII packaged output (gitignored)
```

## Module Conventions

Each construct module follows a consistent pattern:
- `index.ts` — public exports
- `config.ts` — constants, defaults, and type definitions
- Implementation files — one class/construct per file
- `.js` and `.d.ts` files — JSII build output (checked into git)

## shared-config/ — Centralized Platform Config

Contains constants shared across constructs:
- `accounts.ts` — AWS account IDs and stage name type (`BETA | GAMMA | PROD`)
- `networking.ts` — VPC, subnet, security group references
- `s3.ts` — Bucket names per stage
- `secrets.ts` — Secrets Manager paths
- `icav2.ts` — ICAv2 base URLs, token secret IDs
- `event-bridge.ts` — Event bus names
- `slack.ts` — Slack channel configurations
- `database.ts` — Database connection info

## dev/ — Local Development App

A standalone CDK app that imports constructs from `packages/` for hands-on testing:
- Uses `pnpm cdk` commands for synth/deploy
- Not published, workspace-only

## Key Patterns

- **Namespace exports**: Root `index.ts` re-exports modules as namespaces (`export * as lambda from "./lambda"`)
- **Multi-environment**: `StageName` type with account ID lookups in `ACCOUNT_ID_ALIAS` map
- **Layer caching**: Static `Map<Construct, ILayerVersion>` prevents duplicate layer builds per stack
- **Docker bundling**: Python layers use a custom UV-based Docker image for reproducible builds
- **Config-driven defaults**: Constructs provide sensible defaults via `config.ts`, overridable through props
