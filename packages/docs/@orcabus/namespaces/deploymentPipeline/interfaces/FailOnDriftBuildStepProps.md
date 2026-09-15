[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / FailOnDriftBuildStepProps

# Interface: FailOnDriftBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:753](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L753)

## Properties

### accountEnv

> `readonly` **accountEnv**: `Environment`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:758](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L758)

AWS account and region where the drift check runs.
Used to assume the CDK lookup role and set AWS_DEFAULT_REGION.

***

### cdkCommand

> `readonly` **cdkCommand**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:772](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L772)

CDK CLI entrypoint used to run the drift command.
Examples: "pnpm cdk", "pnpm cdk-stateful", "pnpm cdk-stateless".
Must support: "drift <stackId>".

***

### installCommand?

> `readonly` `optional` **installCommand?**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:780](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L780)

Command to install dependencies before running CDK.
If your app is in a subdirectory, prefix with "cd <dir> &&".
Example: "cd dev && pnpm install --frozen-lockfile --ignore-scripts"

#### Default

```ts
DEFAULT_INSTALL_COMMANDS merged with &&.
```

***

### stackId

> `readonly` **stackId**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:766](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L766)

Fully qualified CDK stack ID to check for drift.

Format: `<rootStack>/<constructId>/<envName>/<stackName>`

Example: `DevStack/DeploymentPipeline/OrcaBusBeta/TestStack`
