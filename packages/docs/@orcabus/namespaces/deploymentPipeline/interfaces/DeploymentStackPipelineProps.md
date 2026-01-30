[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStackPipelineProps

# Interface: DeploymentStackPipelineProps

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:136](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L136)

## Properties

### cacheOptions?

> `readonly` `optional` **cacheOptions**: [`CacheOptions`](CacheOptions.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:267](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L267)

Configure the `cache` options for each `CodeBuildStep`. This will allow CodeBuild to use
S3 caching with the `CODEBUILD_CACHE_BUCKET` bucket.

The partial buildspec must still contain definitions for cache paths and keys if used.

#### See

https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.cache

***

### cdkOut?

> `readonly` `optional` **cdkOut**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:192](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L192)

The location where the cdk output will be stored.

#### Default

```ts
cdk.out
```

***

### cdkSynthCmd

> `readonly` **cdkSynthCmd**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:182](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L182)

The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["pnpm install --frozen-lockfile", "pnpm cdk synth"]

***

### driftCheckConfig?

> `readonly` `optional` **driftCheckConfig**: [`DriftCheckConfig`](DriftCheckConfig.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:259](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L259)

Configuration for drift detection checks before deployment.
If specified, the pipeline will check for CloudFormation drift and fail if detected.

***

### enableSlackNotification?

> `readonly` `optional` **enableSlackNotification**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:230](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L230)

Enable notification to the 'alerts-build' slack channel.

#### Default

```ts
True
```

***

### excludedFilePaths?

> `readonly` `optional` **excludedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:178](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L178)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be EXCLUDED from starting the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### githubBranch

> `readonly` **githubBranch**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:143](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L143)

The GitHub branch name the pipeline will listen to.
Avoid using branch names that contain special characters such as parentheses.
Allowed special characters are: "+ - = . _ : / @".
This restriction is due to AWS resource tagging requirements.

***

### githubRepo

> `readonly` **githubRepo**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:147](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L147)

The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`

***

### includedFilePaths?

> `readonly` `optional` **includedFilePaths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:171](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L171)

The list of patterns of Git repository file paths that, when a commit is pushed, are to be INCLUDED as criteria that starts the pipeline.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html

***

### notificationEvents?

> `readonly` `optional` **notificationEvents**: `PipelineNotificationEvents`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:238](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L238)

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

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:164](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L164)

The pipeline name in the bastion account.

***

### reuseExistingArtifactBucket?

> `readonly` `optional` **reuseExistingArtifactBucket**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:246](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L246)

Whether to reuse the existing artifact bucket for cross-deployment pipelines.
If set to true, it will look up the existing artifact bucket in the TOOLCHAIN account.

#### Default

```ts
True
```

***

### stack

> `readonly` **stack**: `any`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:151](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L151)

The stack to which the pipeline will be deploying to its respective account

***

### stackConfig

> `readonly` **stackConfig**: [`StackConfigProps`](StackConfigProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:160](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L160)

The stack configuration/constants that will be passed to the stack props.

***

### stackName

> `readonly` **stackName**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:156](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L156)

The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`

***

### stageEnv?

> `readonly` `optional` **stageEnv**: [`StageEnvProps`](StageEnvProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:225](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L225)

The stage environment for the deployment stack

***

### stripAssemblyAssets?

> `readonly` `optional` **stripAssemblyAssets**: `boolean`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:254](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L254)

Remove assets from the CDK assembly pre-deployment to prevent hitting CodePipeline's 256 MB artifact size limit.
Useful when CDK assets (Lambda code, Docker images, etc.) are large.

#### See

https://github.com/aws/aws-cdk/issues/9917

***

### synthBuildSpec?

> `readonly` `optional` **synthBuildSpec**: `Record`\<`string`, `any`\>

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:199](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L199)

Additional configuration for the CodeBuild step during the CDK synth phase. It will be passed as the
`partialBuildSpec` to the `CodeBuildStep`.

#### Default

```ts
DEFAULT_PARTIAL_BUILD_SPEC
```

***

### synthInstallCommands?

> `readonly` `optional` **synthInstallCommands**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:205](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L205)

The install commands for the synth step.

#### Default

```ts
DEFAULT_INSTALL_COMMANDS
```

***

### synthRolePolicyStatements?

> `readonly` `optional` **synthRolePolicyStatements**: `PolicyStatement`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:186](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L186)

The additional policy statements to add to the CodeBuildStep role during the synth step.

***

### unitAppTestConfig

> `readonly` **unitAppTestConfig**: [`CodeBuildStepProps`](CodeBuildStepProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:213](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L213)

Configuration for the CodeBuild step that runs unit tests for the main application code.
This step will execute in parallel with [unitIacTestConfig](#unitiactestconfig) as part of the synth stage dependencies.
Both must succeed before the synth step runs.

ensure your command includes 'cd' to the main app directory, as the build context starts from the root.

***

### unitIacTestConfig?

> `readonly` `optional` **unitIacTestConfig**: [`CodeBuildStepProps`](CodeBuildStepProps.md)

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:221](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L221)

Configuration for the CodeBuild step that runs unit tests for Infrastructure-as-Code (IaC) at the repository root.
This step will execute in parallel with [unitAppTestConfig](#unitapptestconfig) as part of the synth stage dependencies.
Both must succeed before the synth step runs.

The default command will be from the root of the repo: ["npm install --global corepack@latest", "corepack enable", "make install", "make test"]
