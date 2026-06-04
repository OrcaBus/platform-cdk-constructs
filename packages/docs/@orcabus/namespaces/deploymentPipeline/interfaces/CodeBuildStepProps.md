[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:119](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L119)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:123](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L123)

the main command for the build step to run

***

### installCommands?

> `readonly` `optional` **installCommands?**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:131](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L131)

The install commands to run before the main command.

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec?**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:127](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L127)

Partial buildspec for this CodeBuildStep

***

### rolePolicyStatements?

> `readonly` `optional` **rolePolicyStatements?**: `PolicyStatement`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:135](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L135)

The additional policy statements to add to the CodeBuildStep role.
