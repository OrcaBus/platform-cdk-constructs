[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:116](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L116)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:120](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L120)

the main command for the build step to run

***

### installCommands?

> `readonly` `optional` **installCommands**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:128](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L128)

The install commands to run before the main command.

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:124](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L124)

Partial buildspec for this CodeBuildStep
