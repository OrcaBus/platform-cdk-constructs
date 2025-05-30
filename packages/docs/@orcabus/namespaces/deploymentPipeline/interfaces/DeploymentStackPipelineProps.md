[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:73](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L73)

## Properties

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:118](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L118)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:112](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L112)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["yarn install --immutable", "yarn cdk synth"]

***

### enableSlackNotification?

> `readonly` `optional` **enableSlackNotification**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:133](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L133)

Enable notification to the 'alerts-build' slack channel.

#### Default

```ts
True
```

***

### filePaths?

> `readonly` `optional` **filePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:108](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L108)

The file paths to trigger the pipeline. e.g. ["stateless/**"]

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:80](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L80)

The GitHub branch name the pipeline will listen to.
Avoid using branch names that contain special characters such as parentheses.
Allowed special characters are: "+ - = . _ : / @".
This restriction is due to AWS resource tagging requirements.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:84](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L84)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### notificationEvents?

> `readonly` `optional` **notificationEvents**: `PipelineNotificationEvents`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:141](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L141)

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

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:101](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L101)

The pipeline name in the bastion account.

***

### reuseExistingArtifactBucket?

> `readonly` `optional` **reuseExistingArtifactBucket**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:149](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L149)

Whether to reuse the existing artifact bucket for cross-deployment pipelines.
If set to true, it will look up the existing artifact bucket in the TOOLCHAIN account.

#### Default

```ts
True
```

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:88](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L88)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:97](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L97)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:93](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L93)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:128](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L128)

The stage environment for the deployment stack

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:124](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/deployment-stack-pipeline/pipeline.ts#L124)

Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
```
