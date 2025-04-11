[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../globals.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:69](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L69)

## Properties

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:111](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L111)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:105](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L105)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["yarn install --immutable", "yarn cdk synth"]

***

### filePaths?

> `readonly` `optional` **filePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:101](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L101)

The file paths to trigger the pipeline. e.g. ["stateless/**"]

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:73](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L73)

The github branch name it will listen to.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:77](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L77)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### pipelineName

> `readonly` **pipelineName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:94](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L94)

The pipeline name in the bastion account.

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:81](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L81)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:90](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L90)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:86](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L86)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:121](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L121)

The stage environment for the deployment stack

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:117](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/deployment-stack-pipeline/pipeline.ts#L117)

Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
```
