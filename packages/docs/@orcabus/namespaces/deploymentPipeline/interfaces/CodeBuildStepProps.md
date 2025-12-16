[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CodeBuildStepProps

# Interface: CodeBuildStepProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:82](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L82)

## Properties

### command

> `readonly` **command**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:86](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L86)

the main command for the build step to run

***

### partialBuildSpec?

> `readonly` `optional` **partialBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:90](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L90)

Partial buildspec for this CodeBuildStep
