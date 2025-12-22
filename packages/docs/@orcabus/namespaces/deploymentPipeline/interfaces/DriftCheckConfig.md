[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DriftCheckConfig

# Interface: DriftCheckConfig

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:89](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L89)

Configuration for pre-deployment drift detection checks.

## Properties

### cdkCommand

> `readonly` **cdkCommand**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:95](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L95)

CDK CLI entrypoint used to run the drift command.
Examples: "pnpm cdk", "pnpm cdk-stateful", "pnpm cdk-stateless".
Must support: "drift <stackId>".

***

### installCommand?

> `readonly` `optional` **installCommand**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:103](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L103)

Command to install dependencies before running CDK.
If your app is in a subdirectory, prefix with "cd <dir> &&".
Example: "cd dev && pnpm install --frozen-lockfile --ignore-scripts"

Default: "pnpm install --frozen-lockfile --ignore-scripts"
