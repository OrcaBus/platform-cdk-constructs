[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:117](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L117)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:121](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L121)

the main command for the build step to run

***

### installCommands?

> `readonly` `optional` **installCommands**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:129](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L129)

The install commands to run before the main command.

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:125](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L125)

Partial buildspec for this CodeBuildStep

***

### rolePolicyStatements?

> `readonly` `optional` **rolePolicyStatements**: `PolicyStatement`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:133](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L133)

The additional policy statements to add to the CodeBuildStep role.
