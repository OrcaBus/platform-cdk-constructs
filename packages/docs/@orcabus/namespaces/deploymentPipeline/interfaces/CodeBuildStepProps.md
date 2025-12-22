[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:106](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L106)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:110](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L110)

the main command for the build step to run

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:114](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L114)

Partial buildspec for this CodeBuildStep
