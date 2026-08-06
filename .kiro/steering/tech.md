# Tech Stack & Build System

## Languages

- **TypeScript** (primary) — CDK constructs, compiled via JSII
- **Python** (Lambda layers) — Runtime code packaged as Lambda layers

## Core Frameworks & Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| AWS CDK | 2.244.0 | Infrastructure as Code |
| Constructs | 10.6.0 | CDK construct base |
| JSII | 5.x | Cross-language construct compilation |
| cdk-nag | 2.x | Security/compliance rule checks |
| @aws-cdk/aws-lambda-python-alpha | 2.244.0-alpha.0 | Python Lambda bundling |

## TypeScript Configuration

- Target: ES2022, Module: CommonJS
- Strict mode enabled (noImplicitAny, strictNullChecks, etc.)
- JSII compilation produces `.js` and `.d.ts` alongside `.ts` source (all checked in)

## Python Configuration

- Runtime: Python 3.14, Architecture: ARM64
- Package management: Poetry (layers), Hatchling (test utils)
- Docker-based bundling using a custom UV Dockerfile (`packages/lambda/build_python/`)
- Key libraries: requests, pydantic, fastapi, mangum, pandas, dyntastic

## Package Manager

pnpm 10.28.0 (via corepack). Two workspaces:
- `packages/` — publishable constructs
- `dev/` — development CDK app for testing

## Common Commands

```bash
# Install dependencies
pnpm install

# Build (JSII compile)
pnpm build

# Run tests (Jest)
pnpm test

# Package for distribution
pnpm package

# Publish to npm
pnpm publish

# Generate API documentation
pnpm packages:generate-docs

# Clean all generated files
pnpm clean

# Development CDK commands (from dev/ directory)
cd dev && pnpm cdk <command>
```

## Testing

- **Framework**: Jest 30.x with ts-jest
- **Test location**: `packages/test/`
- **Pattern**: `**/*.test.ts`
- **Python tests**: pytest + moto + hypothesis (in `orcabus-pipeline-test-utils`)

## CI/CD

- **PR checks**: build, package, tests, documentation freshness, pre-commit security (TruffleHog)
- **Release**: GitHub release triggers npm publish via OIDC trusted publisher
- **Node version**: 20.x (CI), 22.x (CodeBuild runtime)

## Documentation

- Auto-generated via typedoc + typedoc-plugin-markdown
- Must be kept in sync — CI fails if docs are stale
- Also indexed on [constructs.dev](https://constructs.dev/packages/@orcabus/platform-cdk-constructs)
