[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:106](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L106)

## Properties

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:158](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L158)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:152](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L152)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["yarn install --immutable", "yarn cdk synth"]

***

### driftCheckConfig?

> `readonly` `optional` **driftCheckConfig**: [`DriftCheckConfig`](DriftCheckConfig.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:202](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L202)

Configuration for drift detection checks before deployment.
If specified, the pipeline will check for CloudFormation drift and fail if detected.

***

### enableSlackNotification?

> `readonly` `optional` **enableSlackNotification**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:173](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L173)

Enable notification to the 'alerts-build' slack channel.

#### Default

```ts
True
```

***

### excludedFilePaths?

> `readonly` `optional` **excludedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:148](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L148)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be EXCLUDED from starting the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:113](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L113)

The GitHub branch name the pipeline will listen to.
Avoid using branch names that contain special characters such as parentheses.
Allowed special characters are: "+ - = . _ : / @".
This restriction is due to AWS resource tagging requirements.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:117](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L117)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### includedFilePaths?

> `readonly` `optional` **includedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:141](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L141)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be INCLUDED as criteria that starts the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### notificationEvents?

> `readonly` `optional` **notificationEvents**: `PipelineNotificationEvents`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:181](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L181)

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

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:134](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L134)

The pipeline name in the bastion account.

***

### reuseExistingArtifactBucket?

> `readonly` `optional` **reuseExistingArtifactBucket**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:189](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L189)

Whether to reuse the existing artifact bucket for cross-deployment pipelines.
If set to true, it will look up the existing artifact bucket in the TOOLCHAIN account.

#### Default

```ts
True
```

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:121](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L121)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:130](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L130)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:126](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L126)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:168](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L168)

The stage environment for the deployment stack

***

### stripAssemblyAssets?

> `readonly` `optional` **stripAssemblyAssets**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:197](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L197)

Remove assets from the CDK assembly pre-deployment to prevent hitting CodePipeline's 256 MB artifact size limit.
Useful when CDK assets (Lambda code, Docker images, etc.) are large.

#### See

https://github.com/aws/aws-cdk/issues/9917

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:164](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L164)

Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
```
