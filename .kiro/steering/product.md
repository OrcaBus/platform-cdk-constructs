# Product Overview

OrcaBus Platform CDK Constructs is a shared library of reusable AWS CDK constructs for the OrcaBus platform, developed by the University of Melbourne Centre for Cancer Research (UMCCR).

## Purpose

Provides opinionated, pre-configured infrastructure building blocks that OrcaBus microservice repositories consume to standardize their AWS deployments. Published to npm as `@orcabus/platform-cdk-constructs`.

## Key Capabilities

- **Multi-account CI/CD pipeline** — CodePipeline with Beta → Gamma → Prod stages, manual approval gates, and drift detection
- **API Gateway** — HTTP API Gateway with Cognito JWT auth, custom domains, and Lambda authorizers
- **Python Lambda packaging** — `PythonUvFunction` construct with optional layers (OrcaBus API tools, ICAv2, Athena/mart, FastAPI)
- **Monitored queues** — SQS with dead-letter queues, CloudWatch alarms, and SNS notifications
- **Custom resource providers** — Framework for database migrations and other custom resources
- **EventBridge rules** — Event routing with Step Functions Slack notifications
- **Shared configuration** — Centralized constants for accounts, networking, secrets, S3, ICAv2, and Slack across environments

## Environments

Three deployment stages: BETA, GAMMA, PROD. All in `ap-southeast-2` (Sydney).

## Consumers

Other OrcaBus microservice repositories install this package as a dependency to build their infrastructure stacks consistently.
