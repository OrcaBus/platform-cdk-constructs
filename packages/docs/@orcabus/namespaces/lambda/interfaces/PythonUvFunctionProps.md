[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [lambda](../README.md) / PythonUvFunctionProps

# Interface: PythonUvFunctionProps

Defined in: [packages/lambda/index.ts:72](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L72)

## Extends

- `PythonFunctionProps`

## Properties

### adotInstrumentation?

> `readonly` `optional` **adotInstrumentation**: `AdotInstrumentationConfig`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:347

Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation

#### See

https://aws-otel.github.io/docs/getting-started/lambda

#### Default

```ts
- No ADOT instrumentation
```

#### Inherited from

`PythonFunctionProps.adotInstrumentation`

***

### allowAllIpv6Outbound?

> `readonly` `optional` **allowAllIpv6Outbound**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:280

Whether to allow the Lambda to send all ipv6 network traffic

If set to true, there will only be a single egress rule which allows all
outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the
Lambda to connect to network targets using ipv6.

Do not specify this property if the `securityGroups` or `securityGroup` property is set.
Instead, configure `allowAllIpv6Outbound` directly on the security group.

#### Default

```ts
false
```

#### Inherited from

`PythonFunctionProps.allowAllIpv6Outbound`

***

### allowAllOutbound?

> `readonly` `optional` **allowAllOutbound**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:267

Whether to allow the Lambda to send all network traffic (except ipv6)

If set to false, you must individually add traffic rules to allow the
Lambda to connect to network targets.

Do not specify this property if the `securityGroups` or `securityGroup` property is set.
Instead, configure `allowAllOutbound` directly on the security group.

#### Default

```ts
true
```

#### Inherited from

`PythonFunctionProps.allowAllOutbound`

***

### allowPublicSubnet?

> `readonly` `optional` **allowPublicSubnet**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:453

Lambda Functions in a public subnet can NOT access the internet.
Use this property to acknowledge this limitation and still place the function in a public subnet.

#### See

https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841

#### Default

```ts
false
```

#### Inherited from

`PythonFunctionProps.allowPublicSubnet`

***

### ~~applicationLogLevel?~~

> `readonly` `optional` **applicationLogLevel**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:513

Sets the application log level for the function.

#### Deprecated

Use `applicationLogLevelV2` as a property instead.

#### Default

```ts
"INFO"
```

#### Inherited from

`PythonFunctionProps.applicationLogLevel`

***

### applicationLogLevelV2?

> `readonly` `optional` **applicationLogLevelV2**: `ApplicationLogLevel`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:518

Sets the application log level for the function.

#### Default

```ts
ApplicationLogLevel.INFO
```

#### Inherited from

`PythonFunctionProps.applicationLogLevelV2`

***

### architecture?

> `readonly` `optional` **architecture**: `Architecture`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:470

The system architectures compatible with this lambda function.

#### Default

```ts
Architecture.X86_64
```

#### Inherited from

`PythonFunctionProps.architecture`

***

### bundling?

> `readonly` `optional` **bundling**: `BundlingOptions`

Defined in: node\_modules/.pnpm/@aws-cdk+aws-lambda-python-alpha@2.208.0-alpha.0\_aws-cdk-lib@2.208.0\_constructs@10.4.2\_\_constructs@10.4.2/node\_modules/@aws-cdk/aws-lambda-python-alpha/lib/function.d.ts:35

Bundling options to use for this function. Use this to specify custom bundling options like
the bundling Docker image, asset hash type, custom hash, architecture, etc.

#### Default

```ts
- Use the default bundling Docker image, with x86_64 architecture.
```

#### Inherited from

`PythonFunctionProps.bundling`

***

### codeSigningConfig?

> `readonly` `optional` **codeSigningConfig**: `ICodeSigningConfig`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:465

Code signing config associated with this function

#### Default

```ts
- Not Sign the Code
```

#### Inherited from

`PythonFunctionProps.codeSigningConfig`

***

### currentVersionOptions?

> `readonly` `optional` **currentVersionOptions**: `VersionOptions`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:439

Options for the `lambda.Version` resource automatically created by the
`fn.currentVersion` method.

#### Default

- default options as described in `VersionOptions`

#### Inherited from

`PythonFunctionProps.currentVersionOptions`

***

### deadLetterQueue?

> `readonly` `optional` **deadLetterQueue**: `IQueue`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:294

The SQS queue to use if DLQ is enabled.
If SNS topic is desired, specify `deadLetterTopic` property instead.

#### Default

- SQS queue with 14 day retention period if `deadLetterQueueEnabled` is `true`

#### Inherited from

`PythonFunctionProps.deadLetterQueue`

***

### deadLetterQueueEnabled?

> `readonly` `optional` **deadLetterQueueEnabled**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:287

Enabled DLQ. If `deadLetterQueue` is undefined,
an SQS queue with default options will be defined for your Function.

#### Default

- false unless `deadLetterQueue` is set, which implies DLQ is enabled.

#### Inherited from

`PythonFunctionProps.deadLetterQueueEnabled`

***

### deadLetterTopic?

> `readonly` `optional` **deadLetterTopic**: `ITopic`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:302

The SNS topic to use as a DLQ.
Note that if `deadLetterQueueEnabled` is set to `true`, an SQS queue will be created
rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

#### Default

```ts
- no SNS topic
```

#### Inherited from

`PythonFunctionProps.deadLetterTopic`

***

### description?

> `readonly` `optional` **description**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:150

A description of the function.

#### Default

```ts
- No description.
```

#### Inherited from

`PythonFunctionProps.description`

***

### entry

> `readonly` **entry**: `string`

Defined in: node\_modules/.pnpm/@aws-cdk+aws-lambda-python-alpha@2.208.0-alpha.0\_aws-cdk-lib@2.208.0\_constructs@10.4.2\_\_constructs@10.4.2/node\_modules/@aws-cdk/aws-lambda-python-alpha/lib/function.d.ts:11

Path to the source of the function or the location for dependencies.

#### Inherited from

`PythonFunctionProps.entry`

***

### environment?

> `readonly` `optional` **environment**: `object`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:167

Key-value pairs that Lambda caches and makes available for your Lambda
functions. Use environment variables to apply configuration changes, such
as test and production environment configurations, without changing your
Lambda function source code.

#### Index Signature

\[`key`: `string`\]: `string`

#### Default

```ts
- No environment variables.
```

#### Inherited from

`PythonFunctionProps.environment`

***

### environmentEncryption?

> `readonly` `optional` **environmentEncryption**: `IKey`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:459

The AWS KMS key that's used to encrypt your function's environment variables.

#### Default

```ts
- AWS Lambda creates and uses an AWS managed customer master key (CMK).
```

#### Inherited from

`PythonFunctionProps.environmentEncryption`

***

### ephemeralStorageSize?

> `readonly` `optional` **ephemeralStorageSize**: `Size`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:191

The size of the function’s /tmp directory in MiB.

#### Default

```ts
512 MiB
```

#### Inherited from

`PythonFunctionProps.ephemeralStorageSize`

***

### events?

> `readonly` `optional` **events**: `IEventSource`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:378

Event sources for this function.

You can also add event sources using `addEventSource`.

#### Default

```ts
- No event sources.
```

#### Inherited from

`PythonFunctionProps.events`

***

### filesystem?

> `readonly` `optional` **filesystem**: `FileSystem`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:445

The filesystem configuration for the lambda function

#### Default

```ts
- will not mount any filesystem
```

#### Inherited from

`PythonFunctionProps.filesystem`

***

### functionName?

> `readonly` `optional` **functionName**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:176

A name for the function.

#### Default

```ts
- AWS CloudFormation generates a unique physical ID and uses that
ID for the function's name. For more information, see Name Type.
```

#### Inherited from

`PythonFunctionProps.functionName`

***

### handler?

> `readonly` `optional` **handler**: `string`

Defined in: node\_modules/.pnpm/@aws-cdk+aws-lambda-python-alpha@2.208.0-alpha.0\_aws-cdk-lib@2.208.0\_constructs@10.4.2\_\_constructs@10.4.2/node\_modules/@aws-cdk/aws-lambda-python-alpha/lib/function.d.ts:28

The name of the exported handler in the index file.

#### Default

```ts
handler
```

#### Inherited from

`PythonFunctionProps.handler`

***

### icav2Resources?

> `readonly` `optional` **icav2Resources**: [`Icav2ResourcesProps`](Icav2ResourcesProps.md)

Defined in: [packages/lambda/index.ts:113](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L113)

Provide the icav2Resources, optional, otherwise it will default to
@DEFAULT_ICAV2_ACCESS_TOKEN_SECRET_ID for the secret

***

### includeFastApiLayer?

> `readonly` `optional` **includeFastApiLayer**: `boolean`

Defined in: [packages/lambda/index.ts:93](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L93)

Whether or not to include the fastapi layer in the lambda function build

***

### includeIcav2Layer?

> `readonly` `optional` **includeIcav2Layer**: `boolean`

Defined in: [packages/lambda/index.ts:88](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L88)

Whether or not to include the icav2 layer in the lambda function build

***

### includeMartLayer?

> `readonly` `optional` **includeMartLayer**: `boolean`

Defined in: [packages/lambda/index.ts:83](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L83)

Whether or not to include the mart layer in the lambda function build
Note that the mart layer is a little heavier than the orcabus api tools layer
Since we require pandas to be installed

***

### includeOrcabusApiToolsLayer?

> `readonly` `optional` **includeOrcabusApiToolsLayer**: `boolean`

Defined in: [packages/lambda/index.ts:76](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L76)

Whether or not to include the orcabus api tools layer in the lambda function build

***

### index?

> `readonly` `optional` **index**: `string`

Defined in: node\_modules/.pnpm/@aws-cdk+aws-lambda-python-alpha@2.208.0-alpha.0\_aws-cdk-lib@2.208.0\_constructs@10.4.2\_\_constructs@10.4.2/node\_modules/@aws-cdk/aws-lambda-python-alpha/lib/function.d.ts:22

The path (relative to entry) to the index file containing the exported handler.

#### Default

```ts
index.py
```

#### Inherited from

`PythonFunctionProps.index`

***

### initialPolicy?

> `readonly` `optional` **initialPolicy**: `PolicyStatement`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:199

Initial policy statements to add to the created Lambda Role.

You can call `addToRolePolicy` to the created lambda to add statements post creation.

#### Default

```ts
- No policy statements are added to the created Lambda role.
```

#### Inherited from

`PythonFunctionProps.initialPolicy`

***

### insightsVersion?

> `readonly` `optional` **insightsVersion**: `LambdaInsightsVersion`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:340

Specify the version of CloudWatch Lambda insights to use for monitoring

#### See

 - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html

When used with `DockerImageFunction` or `DockerImageCode`, the Docker image should have
the Lambda insights agent installed.
 - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html

#### Default

```ts
- No Lambda Insights
```

#### Inherited from

`PythonFunctionProps.insightsVersion`

***

### ipv6AllowedForDualStack?

> `readonly` `optional` **ipv6AllowedForDualStack**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:233

Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets.

Only used if 'vpc' is supplied.

#### Default

```ts
false
```

#### Inherited from

`PythonFunctionProps.ipv6AllowedForDualStack`

***

### layers?

> `readonly` `optional` **layers**: `ILayerVersion`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:363

A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in
additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
that can be used by multiple functions.

#### Default

```ts
- No layers.
```

#### Inherited from

`PythonFunctionProps.layers`

***

### ~~logFormat?~~

> `readonly` `optional` **logFormat**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:495

Sets the logFormat for the function.

#### Deprecated

Use `loggingFormat` as a property instead.

#### Default

```ts
"Text"
```

#### Inherited from

`PythonFunctionProps.logFormat`

***

### loggingFormat?

> `readonly` `optional` **loggingFormat**: `LoggingFormat`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:500

Sets the loggingFormat for the function.

#### Default

```ts
LoggingFormat.TEXT
```

#### Inherited from

`PythonFunctionProps.loggingFormat`

***

### logGroup?

> `readonly` `optional` **logGroup**: `ILogGroup`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:489

The log group the function sends logs to.

By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/\<function name\>.
However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention.

Use the `logGroup` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it.

Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16.
If you are deploying to another type of region, please check regional availability first.

#### Default

`/aws/lambda/${this.functionName}` - default log group created by Lambda

#### Inherited from

`PythonFunctionProps.logGroup`

***

### ~~logRemovalPolicy?~~

> `readonly` `optional` **logRemovalPolicy**: `RemovalPolicy`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:413

Determine the removal policy of the log group that is auto-created by this construct.

Normally you want to retain the log group so you can diagnose issues
from logs even after a deployment that no longer includes the log group.
In that case, use the normal date-based retention policy to age out your
logs.

#### Deprecated

use `logGroup` instead

#### Default

```ts
RemovalPolicy.Retain
```

#### Inherited from

`PythonFunctionProps.logRemovalPolicy`

***

### ~~logRetention?~~

> `readonly` `optional` **logRetention**: `RetentionDays`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:401

The number of days log events are kept in CloudWatch Logs. When updating
this property, unsetting it doesn't remove the log retention policy. To
remove the retention policy, set the value to `INFINITE`.

This is a legacy API and we strongly recommend you move away from it if you can.
Instead create a fully customizable log group with `logs.LogGroup` and use the `logGroup` property
to instruct the Lambda function to send logs to it.
Migrating from `logRetention` to `logGroup` will cause the name of the log group to change.
Users and code and referencing the name verbatim will have to adjust.

In AWS CDK code, you can access the log group name directly from the LogGroup construct:
```ts
import * as logs from 'aws-cdk-lib/aws-logs';

declare const myLogGroup: logs.LogGroup;
myLogGroup.logGroupName;
```

#### Deprecated

use `logGroup` instead

#### Default

```ts
logs.RetentionDays.INFINITE
```

#### Inherited from

`PythonFunctionProps.logRetention`

***

### logRetentionRetryOptions?

> `readonly` `optional` **logRetentionRetryOptions**: `LogRetentionRetryOptions`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:433

When log retention is specified, a custom resource attempts to create the CloudWatch log group.
These options control the retry policy when interacting with CloudWatch APIs.

This is a legacy API and we strongly recommend you migrate to `logGroup` if you can.
`logGroup` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

#### Default

```ts
- Default AWS SDK retry options.
```

#### Inherited from

`PythonFunctionProps.logRetentionRetryOptions`

***

### logRetentionRole?

> `readonly` `optional` **logRetentionRole**: `IRole`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:423

The IAM role for the Lambda function associated with the custom resource
that sets the retention policy.

This is a legacy API and we strongly recommend you migrate to `logGroup` if you can.
`logGroup` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

#### Default

```ts
- A new role is created.
```

#### Inherited from

`PythonFunctionProps.logRetentionRole`

***

### martEnvironmentVariables?

> `readonly` `optional` **martEnvironmentVariables**: [`MartEnvironmentVariables`](MartEnvironmentVariables.md)

Defined in: [packages/lambda/index.ts:107](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L107)

Provide the martEnvironmentVariables, optional, otherwise it will default to
@MART_ENV_VARS.ATHENA_WORKGROUP_NAME, @MART_ENV_VARS.ATHENA_DATASOURCE_NAME
and @MART_ENV_VARS.ATHENA_DATABASE_NAME for the athena workgroup, datasource and database respectively

***

### maxEventAge?

> `readonly` `optional` **maxEventAge**: `Duration`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/event-invoke-config.d.ts:30

The maximum age of a request that Lambda sends to a function for
processing.

Minimum: 60 seconds
Maximum: 6 hours

#### Default

```ts
Duration.hours(6)
```

#### Inherited from

`PythonFunctionProps.maxEventAge`

***

### memorySize?

> `readonly` `optional` **memorySize**: `number`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:185

The amount of memory, in MB, that is allocated to your Lambda function.
Lambda uses this value to proportionally allocate the amount of CPU
power. For more information, see Resource Model in the AWS Lambda
Developer Guide.

#### Default

```ts
128
```

#### Inherited from

`PythonFunctionProps.memorySize`

***

### onFailure?

> `readonly` `optional` **onFailure**: `IDestination`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/event-invoke-config.d.ts:14

The destination for failed invocations.

#### Default

```ts
- no destination
```

#### Inherited from

`PythonFunctionProps.onFailure`

***

### onSuccess?

> `readonly` `optional` **onSuccess**: `IDestination`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/event-invoke-config.d.ts:20

The destination for successful invocations.

#### Default

```ts
- no destination
```

#### Inherited from

`PythonFunctionProps.onSuccess`

***

### orcabusTokenResources?

> `readonly` `optional` **orcabusTokenResources**: [`OrcabusResourcesProps`](OrcabusResourcesProps.md)

Defined in: [packages/lambda/index.ts:100](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/lambda/index.ts#L100)

Provide the orcabusTokenResources, optional, otherwise it will default to
@DEFAULT_ORCABUS_TOKEN_SECRET_ID and @DEFAULT_HOSTNAME_SSM_PARAMETER
for the secret and SSM parameter respectively

***

### paramsAndSecrets?

> `readonly` `optional` **paramsAndSecrets**: `ParamsAndSecretsLayerVersion`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:355

Specify the configuration of Parameters and Secrets Extension

#### See

 - https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html
 - https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html

#### Default

```ts
- No Parameters and Secrets Extension
```

#### Inherited from

`PythonFunctionProps.paramsAndSecrets`

***

### profiling?

> `readonly` `optional` **profiling**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:322

Enable profiling.

#### See

https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html

#### Default

```ts
- No profiling.
```

#### Inherited from

`PythonFunctionProps.profiling`

***

### profilingGroup?

> `readonly` `optional` **profilingGroup**: `IProfilingGroup`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:329

Profiling Group.

#### See

https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html

#### Default

- A new profiling group will be created if `profiling` is set.

#### Inherited from

`PythonFunctionProps.profilingGroup`

***

### recursiveLoop?

> `readonly` `optional` **recursiveLoop**: `RecursiveLoop`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:507

Sets the Recursive Loop Protection for Lambda Function.
It lets Lambda detect and terminate unintended recursive loops.

#### Default

```ts
RecursiveLoop.Terminate
```

#### Inherited from

`PythonFunctionProps.recursiveLoop`

***

### reservedConcurrentExecutions?

> `readonly` `optional` **reservedConcurrentExecutions**: `number`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:370

The maximum of concurrent executions you want to reserve for the function.

#### Default

```ts
- No specific limit - account limit.
```

#### See

https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html

#### Inherited from

`PythonFunctionProps.reservedConcurrentExecutions`

***

### retryAttempts?

> `readonly` `optional` **retryAttempts**: `number`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/event-invoke-config.d.ts:39

The maximum number of times to retry when the function returns an error.

Minimum: 0
Maximum: 2

#### Default

```ts
2
```

#### Inherited from

`PythonFunctionProps.retryAttempts`

***

### role?

> `readonly` `optional` **role**: `IRole`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:216

Lambda execution role.

This is the role that will be assumed by the function upon execution.
It controls the permissions that the function will have. The Role must
be assumable by the 'lambda.amazonaws.com' service principal.

The default Role automatically has permissions granted for Lambda execution. If you
provide a Role, you must add the relevant AWS managed policies yourself.

The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
"service-role/AWSLambdaVPCAccessExecutionRole".

#### Default

- A unique role will be generated for this lambda function.
Both supplied and generated roles can always be changed by calling `addToRolePolicy`.

#### Inherited from

`PythonFunctionProps.role`

***

### runtime

> `readonly` **runtime**: `Runtime`

Defined in: node\_modules/.pnpm/@aws-cdk+aws-lambda-python-alpha@2.208.0-alpha.0\_aws-cdk-lib@2.208.0\_constructs@10.4.2\_\_constructs@10.4.2/node\_modules/@aws-cdk/aws-lambda-python-alpha/lib/function.d.ts:16

The runtime environment. Only runtimes of the Python family are
supported.

#### Inherited from

`PythonFunctionProps.runtime`

***

### runtimeManagementMode?

> `readonly` `optional` **runtimeManagementMode**: `RuntimeManagementMode`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:475

Sets the runtime management configuration for a function's version.

#### Default

```ts
Auto
```

#### Inherited from

`PythonFunctionProps.runtimeManagementMode`

***

### securityGroups?

> `readonly` `optional` **securityGroups**: `ISecurityGroup`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:255

The list of security groups to associate with the Lambda's network interfaces.

Only used if 'vpc' is supplied.

#### Default

```ts
- If the function is placed within a VPC and a security group is
not specified, either by this or securityGroup prop, a dedicated security
group will be created for this function.
```

#### Inherited from

`PythonFunctionProps.securityGroups`

***

### snapStart?

> `readonly` `optional` **snapStart**: `SnapStartConf`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:315

Enable SnapStart for Lambda Function.
SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime

#### Default

```ts
- No snapstart
```

#### Inherited from

`PythonFunctionProps.snapStart`

***

### ~~systemLogLevel?~~

> `readonly` `optional` **systemLogLevel**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:524

Sets the system log level for the function.

#### Deprecated

Use `systemLogLevelV2` as a property instead.

#### Default

```ts
"INFO"
```

#### Inherited from

`PythonFunctionProps.systemLogLevel`

***

### systemLogLevelV2?

> `readonly` `optional` **systemLogLevelV2**: `SystemLogLevel`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:529

Sets the system log level for the function.

#### Default

```ts
SystemLogLevel.INFO
```

#### Inherited from

`PythonFunctionProps.systemLogLevelV2`

***

### timeout?

> `readonly` `optional` **timeout**: `Duration`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:158

The function execution time (in seconds) after which Lambda terminates
the function. Because the execution time affects cost, set this value
based on the function's expected execution time.

#### Default

```ts
Duration.seconds(3)
```

#### Inherited from

`PythonFunctionProps.timeout`

***

### tracing?

> `readonly` `optional` **tracing**: `Tracing`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:308

Enable AWS X-Ray Tracing for Lambda Function.

#### Default

```ts
Tracing.Disabled
```

#### Inherited from

`PythonFunctionProps.tracing`

***

### vpc?

> `readonly` `optional` **vpc**: `IVpc`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:225

VPC network to place Lambda network interfaces

Specify this if the Lambda function needs to access resources in a VPC.
This is required when `vpcSubnets` is specified.

#### Default

```ts
- Function is not placed within a VPC.
```

#### Inherited from

`PythonFunctionProps.vpc`

***

### vpcSubnets?

> `readonly` `optional` **vpcSubnets**: `SubnetSelection`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.208.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:245

Where to place the network interfaces within the VPC.

This requires `vpc` to be specified in order for interfaces to actually be
placed in the subnets. If `vpc` is not specify, this will raise an error.

Note: Internet access for Lambda Functions requires a NAT Gateway, so picking
public subnets is not allowed (unless `allowPublicSubnet` is set to `true`).

#### Default

```ts
- the Vpc default strategy if not specified
```

#### Inherited from

`PythonFunctionProps.vpcSubnets`
