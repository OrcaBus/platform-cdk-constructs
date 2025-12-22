[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / FailOnDriftBuildStepProps

# Interface: FailOnDriftBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:553](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L553)

## Properties

### accountEnv

> `readonly` **accountEnv**: `Environment`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:558](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L558)

AWS account and region where the drift check runs.
Used to assume the CDK lookup role and set AWS_DEFAULT_REGION.

***

### cdkCommand

> `readonly` **cdkCommand**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:572](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L572)

CDK CLI entrypoint used to run the drift command.
Examples: "pnpm cdk", "pnpm cdk-stateful", "pnpm cdk-stateless".
Must support: "drift <stackId>".

***

### installCommand?

> `readonly` `optional` **installCommand**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:580](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L580)

Command to install dependencies before running CDK.
If your app is in a subdirectory, prefix with "cd <dir> &&".
Example: "cd dev && pnpm install --frozen-lockfile --ignore-scripts"

Default: "pnpm install --frozen-lockfile --ignore-scripts"

***

### stackId

> `readonly` **stackId**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:566](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L566)

Fully qualified CDK stack ID to check for drift.

Format: `<rootStack>/<constructId>/<envName>/<stackName>`

Example: `DevStack/DeploymentPipeline/OrcaBusBeta/TestStack`
