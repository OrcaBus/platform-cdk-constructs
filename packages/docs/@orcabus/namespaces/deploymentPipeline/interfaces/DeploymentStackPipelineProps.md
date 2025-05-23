[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:72](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L72)

## Properties

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:114](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L114)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:108](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L108)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["yarn install --immutable", "yarn cdk synth"]

***

### enableSlackNotification?

> `readonly` `optional` **enableSlackNotification**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:129](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L129)

Enable notification to the 'alerts-build' slack channel.

#### Default

```ts
True
```

***

### filePaths?

> `readonly` `optional` **filePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:104](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L104)

The file paths to trigger the pipeline. e.g. ["stateless/**"]

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:76](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L76)

The github branch name it will listen to.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:80](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L80)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### notificationEvents?

> `readonly` `optional` **notificationEvents**: `PipelineNotificationEvents`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:137](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L137)

The pipeline notification events that will trigger a Slack channel notification.
Only applies if `enableSlackNotification` is set to true.

#### Default

```ts
[PipelineNotificationEvents.PIPELINE_EXECUTION_FAILED] –
  Only failed pipeline executions will trigger a notification.
```

***

### pipelineName

> `readonly` **pipelineName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:97](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L97)

The pipeline name in the bastion account.

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:84](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L84)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:93](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L93)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:89](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L89)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:124](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L124)

The stage environment for the deployment stack

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:120](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/deployment-stack-pipeline/pipeline.ts#L120)

Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
```
