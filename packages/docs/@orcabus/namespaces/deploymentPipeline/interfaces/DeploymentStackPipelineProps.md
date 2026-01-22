[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:119](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L119)

## Properties

### cacheOptions?

> `readonly` `optional` **cacheOptions**: [`CacheOptions`](CacheOptions.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:239](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L239)

Configure the `cache` options for each `CodeBuildStep`. This will allow CodeBuild to use
S3 caching with the `CODEBUILD_CACHE_BUCKET` bucket.

The partial buildspec must still contain definitions for cache paths and keys if used.

#### See

https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.cache

***

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:171](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L171)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:165](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L165)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["pnpm install --frozen-lockfile", "pnpm cdk synth"]

***

### driftCheckConfig?

> `readonly` `optional` **driftCheckConfig**: [`DriftCheckConfig`](DriftCheckConfig.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:231](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L231)

Configuration for drift detection checks before deployment.
If specified, the pipeline will check for CloudFormation drift and fail if detected.

***

### enableSlackNotification?

> `readonly` `optional` **enableSlackNotification**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:202](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L202)

Enable notification to the 'alerts-build' slack channel.

#### Default

```ts
True
```

***

### excludedFilePaths?

> `readonly` `optional` **excludedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:161](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L161)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be EXCLUDED from starting the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:126](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L126)

The GitHub branch name the pipeline will listen to.
Avoid using branch names that contain special characters such as parentheses.
Allowed special characters are: "+ - = . _ : / @".
This restriction is due to AWS resource tagging requirements.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:130](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L130)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### includedFilePaths?

> `readonly` `optional` **includedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:154](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L154)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be INCLUDED as criteria that starts the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### notificationEvents?

> `readonly` `optional` **notificationEvents**: `PipelineNotificationEvents`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:210](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L210)

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

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:147](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L147)

The pipeline name in the bastion account.

***

### reuseExistingArtifactBucket?

> `readonly` `optional` **reuseExistingArtifactBucket**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:218](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L218)

Whether to reuse the existing artifact bucket for cross-deployment pipelines.
If set to true, it will look up the existing artifact bucket in the TOOLCHAIN account.

#### Default

```ts
True
```

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:134](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L134)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:143](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L143)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:139](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L139)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:197](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L197)

The stage environment for the deployment stack

***

### stripAssemblyAssets?

> `readonly` `optional` **stripAssemblyAssets**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:226](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L226)

Remove assets from the CDK assembly pre-deployment to prevent hitting CodePipeline's 256 MB artifact size limit.
Useful when CDK assets (Lambda code, Docker images, etc.) are large.

#### See

https://github.com/aws/aws-cdk/issues/9917

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:177](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L177)

Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
```

***

### unitAppTestConfig

> `readonly` **unitAppTestConfig**: [`CodeBuildStepProps`](CodeBuildStepProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:185](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L185)

Configuration for the CodeBuild step that runs unit tests for the main application code.
This step will execute in parallel with [unitIacTestConfig](#unitiactestconfig) as part of the synth stage dependencies.
Both must succeed before the synth step runs.

ensure your command includes 'cd' to the main app directory, as the build context starts from the root.

***

### unitIacTestConfig?

> `readonly` `optional` **unitIacTestConfig**: [`CodeBuildStepProps`](CodeBuildStepProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:193](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L193)

Configuration for the CodeBuild step that runs unit tests for Infrastructure-as-Code (IaC) at the repository root.
This step will execute in parallel with [unitAppTestConfig](#unitapptestconfig) as part of the synth stage dependencies.
Both must succeed before the synth step runs.

The default command will be from the root of the repo: ["npm install --global corepack@latest", "corepack enable", "make install", "make test"]
