[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:118](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L118)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:122](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L122)

the main command for the build step to run

***

### installCommands?

> `readonly` `optional` **installCommands?**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:130](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L130)

The install commands to run before the main command.

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec?**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:126](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L126)

Partial buildspec for this CodeBuildStep

***

### rolePolicyStatements?

> `readonly` `optional` **rolePolicyStatements?**: `PolicyStatement`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:134](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L134)

The additional policy statements to add to the CodeBuildStep role.
