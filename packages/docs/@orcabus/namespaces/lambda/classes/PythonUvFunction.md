[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [lambda](../README.md) / PythonUvFunction

# Class: PythonUvFunction

Defined in: [packages/lambda/index.ts:112](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/lambda/index.ts#L112)

## Extends

- `PythonFunction`

## Constructors

### Constructor

> **new PythonUvFunction**(`scope`, `id`, `props`): `PythonUvFunction`

Defined in: [packages/lambda/index.ts:120](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/lambda/index.ts#L120)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`PythonUvFunctionProps`](../interfaces/PythonUvFunctionProps.md)

#### Returns

`PythonUvFunction`

#### Overrides

`PythonFunction.constructor`

## Properties

### \_connections?

> `protected` `optional` **\_connections**: `Connections`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:248

**`Internal`**

Actual connections object for this Lambda

May be unset, in which case this Lambda is not configured use in a VPC.

#### Inherited from

`PythonFunction._connections`

***

### \_functionUrlInvocationGrants

> `protected` **\_functionUrlInvocationGrants**: `Record`\<`string`, `Grant`\>

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:264

**`Internal`**

Mapping of function URL invocation principals to grants. Used to de-dupe `grantInvokeUrl()` calls.

#### Inherited from

`PythonFunction._functionUrlInvocationGrants`

***

### \_invocationGrants

> `protected` **\_invocationGrants**: `Record`\<`string`, `Grant`\>

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:259

**`Internal`**

Mapping of invocation principals to grants. Used to de-dupe `grantInvoke()` calls.

#### Inherited from

`PythonFunction._invocationGrants`

***

### \_layers

> `readonly` **\_layers**: `ILayerVersion`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:683

**`Internal`**

#### Inherited from

`PythonFunction._layers`

***

### \_logRetention?

> `optional` **\_logRetention**: `LogRetention`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:685

**`Internal`**

#### Inherited from

`PythonFunction._logRetention`

***

### \_skipPermissions?

> `protected` `readonly` `optional` **\_skipPermissions**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:241

**`Internal`**

Whether the user decides to skip adding permissions.
The only use case is for cross-account, imported lambdas
where the user commits to modifying the permisssions
on the imported lambda outside CDK.

#### Inherited from

`PythonFunction._skipPermissions`

***

### \_warnIfCurrentVersionCalled

> `protected` **\_warnIfCurrentVersionCalled**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:254

**`Internal`**

Flag to delay adding a warning message until current version is invoked.

#### Inherited from

`PythonFunction._warnIfCurrentVersionCalled`

***

### architecture

> `readonly` **architecture**: `Architecture`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:675

The architecture of this Lambda Function (this is an optional attribute and defaults to X86_64).

#### Inherited from

`PythonFunction.architecture`

***

### canCreatePermissions

> `protected` `readonly` **canCreatePermissions**: `true` = `true`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:681

Whether the addPermission() call adds any permissions

True for new Lambdas, false for version $LATEST and imported Lambdas
from different accounts.

#### Inherited from

`PythonFunction.canCreatePermissions`

***

### deadLetterQueue?

> `readonly` `optional` **deadLetterQueue**: `IQueue`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:667

The DLQ (as queue) associated with this Lambda Function (this is an optional attribute).

#### Inherited from

`PythonFunction.deadLetterQueue`

***

### deadLetterTopic?

> `readonly` `optional` **deadLetterTopic**: `ITopic`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:671

The DLQ (as topic) associated with this Lambda Function (this is an optional attribute).

#### Inherited from

`PythonFunction.deadLetterTopic`

***

### env

> `readonly` **env**: `ResourceEnvironment`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:111

The environment this resource belongs to.
For resources that are created and managed by the CDK
(generally, those created by creating new class instances like Role, Bucket, etc.),
this is always the same as the environment of the stack they belong to;
however, for imported resources
(those obtained from static methods like fromRoleArn, fromBucketName, etc.),
that might be different than the stack they were imported into.

#### Inherited from

`PythonFunction.env`

***

### functionArn

> `readonly` **functionArn**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:651

ARN of this function

#### Inherited from

`PythonFunction.functionArn`

***

### functionName

> `readonly` **functionName**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:647

Name of this function

#### Inherited from

`PythonFunction.functionName`

***

### grantPrincipal

> `readonly` **grantPrincipal**: `IPrincipal`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:663

The principal this Lambda Function is running as

#### Inherited from

`PythonFunction.grantPrincipal`

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

The tree node.

#### Inherited from

`PythonFunction.node`

***

### permissionsNode

> `readonly` **permissionsNode**: `Node`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:680

The construct node where permissions are attached.

#### Inherited from

`PythonFunction.permissionsNode`

***

### physicalName

> `protected` `readonly` **physicalName**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:123

Returns a string-encoded token that resolves to the physical name that
should be passed to the CloudFormation resource.

This value will resolve to one of the following:
- a concrete value (e.g. `"my-awesome-bucket"`)
- `undefined`, when a name should be generated by CloudFormation
- a concrete name generated automatically during synthesis, in
  cross-environment scenarios.

#### Inherited from

`PythonFunction.physicalName`

***

### role?

> `readonly` `optional` **role**: `IRole`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:655

Execution role associated with this function

#### Inherited from

`PythonFunction.role`

***

### runtime

> `readonly` **runtime**: `Runtime`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:659

The runtime configured for this lambda.

#### Inherited from

`PythonFunction.runtime`

***

### stack

> `readonly` **stack**: `Stack`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:110

The stack in which this resource is defined.

#### Inherited from

`PythonFunction.stack`

***

### timeout?

> `readonly` `optional` **timeout**: `Duration`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:679

The timeout configured for this lambda.

#### Inherited from

`PythonFunction.timeout`

***

### \_VER\_PROPS

> `static` **\_VER\_PROPS**: `object`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:570

**`Internal`**

#### Index Signature

\[`key`: `string`\]: `boolean`

#### Inherited from

`PythonFunction._VER_PROPS`

## Accessors

### connections

#### Get Signature

> **get** **connections**(): `Connections`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:295

Access the Connections object

Will fail if not a VPC-enabled Lambda Function

##### Returns

`Connections`

#### Inherited from

`PythonFunction.connections`

***

### currentVersion

#### Get Signature

> **get** **currentVersion**(): `Version`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:567

Returns a `lambda.Version` which represents the current version of this
Lambda function. A new version will be created every time the function's
configuration changes.

You can specify options for this version using the `currentVersionOptions`
prop when initializing the `lambda.Function`.

##### Returns

`Version`

#### Inherited from

`PythonFunction.currentVersion`

***

### isBoundToVpc

#### Get Signature

> **get** **isBoundToVpc**(): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:302

Whether or not this Lambda function was bound to a VPC

If this is is `false`, trying to access the `connections` object will fail.

##### Returns

`boolean`

#### Inherited from

`PythonFunction.isBoundToVpc`

***

### latestVersion

#### Get Signature

> **get** **latestVersion**(): `IVersion`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:296

The `$LATEST` version of this function.

Note that this is reference to a non-specific AWS Lambda version, which
means the function this version refers to can return different results in
different invocations.

To obtain a reference to an explicit version which references the current
function configuration, use `lambdaFunction.currentVersion` instead.

##### Returns

`IVersion`

#### Inherited from

`PythonFunction.latestVersion`

***

### logGroup

#### Get Signature

> **get** **logGroup**(): `ILogGroup`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:770

The LogGroup where the Lambda function's logs are made available.

If either `logRetention` is set or this property is called, a CloudFormation custom resource is added to the stack that
pre-creates the log group as part of the stack deployment, if it already doesn't exist, and sets the correct log retention
period (never expire, by default).

Further, if the log group already exists and the `logRetention` is not set, the custom resource will reset the log retention
to never expire even if it was configured with a different value.

##### Returns

`ILogGroup`

#### Inherited from

`PythonFunction.logGroup`

***

### resourceArnsForGrantInvoke

#### Get Signature

> **get** **resourceArnsForGrantInvoke**(): `string`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:568

The ARN(s) to put into the resource field of the generated IAM policy for grantInvoke()

##### Returns

`string`[]

#### Inherited from

`PythonFunction.resourceArnsForGrantInvoke`

## Methods

### \_checkEdgeCompatibility()

> **\_checkEdgeCompatibility**(): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:772

**`Internal`**

#### Returns

`void`

#### Inherited from

`PythonFunction._checkEdgeCompatibility`

***

### \_enableCrossEnvironment()

> **\_enableCrossEnvironment**(): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:135

**`Internal`**

Called when this resource is referenced across environments
(account/region) to order to request that a physical name will be generated
for this resource during synthesis, so the resource can be referenced
through its absolute name/arn.

#### Returns

`void`

#### Inherited from

`PythonFunction._enableCrossEnvironment`

***

### \_functionNode()

> `protected` **\_functionNode**(): `Node`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:333

**`Internal`**

Returns the construct tree node that corresponds to the lambda function.
For use internally for constructs, when the tree is set up in non-standard ways. Ex: SingletonFunction.

#### Returns

`Node`

#### Inherited from

`PythonFunction._functionNode`

***

### \_isStackAccount()

> `protected` **\_isStackAccount**(): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:348

**`Internal`**

Given the function arn, check if the account id matches this account

Function ARNs look like this:

  arn:aws:lambda:region:account-id:function:function-name

..which means that in order to extract the `account-id` component from the ARN, we can
split the ARN using ":" and select the component in index 4.

#### Returns

`boolean`

true if account id of function matches the account specified on the stack, false otherwise.

#### Inherited from

`PythonFunction._isStackAccount`

***

### addAlias()

> **addAlias**(`aliasName`, `options?`): `Alias`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:759

Defines an alias for this function.

The alias will automatically be updated to point to the latest version of
the function as it is being updated during a deployment.

```ts
declare const fn: lambda.Function;

fn.addAlias('Live');

// Is equivalent to

new lambda.Alias(this, 'AliasLive', {
  aliasName: 'Live',
  version: fn.currentVersion,
});
```

#### Parameters

##### aliasName

`string`

The name of the alias

##### options?

`AliasOptions`

Alias options

#### Returns

`Alias`

#### Inherited from

`PythonFunction.addAlias`

***

### addEnvironment()

> **addEnvironment**(`key`, `value`, `options?`): `this`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:703

Adds an environment variable to this Lambda function.
If this is a ref to a Lambda function, this operation results in a no-op.

#### Parameters

##### key

`string`

The environment variable key.

##### value

`string`

The environment variable's value.

##### options?

`EnvironmentOptions`

Environment variable options.

#### Returns

`this`

#### Inherited from

`PythonFunction.addEnvironment`

***

### addEventSource()

> **addEventSource**(`source`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:325

Adds an event source to this function.

Event sources are implemented in the aws-cdk-lib/aws-lambda-event-sources module.

The following example adds an SQS Queue as an event source:
```
import { SqsEventSource } from 'aws-cdk-lib/aws-lambda-event-sources';
myFunction.addEventSource(new SqsEventSource(myQueue));
```

#### Parameters

##### source

`IEventSource`

#### Returns

`void`

#### Inherited from

`PythonFunction.addEventSource`

***

### addEventSourceMapping()

> **addEventSourceMapping**(`id`, `options`): `EventSourceMapping`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:303

Adds an event source that maps to this AWS Lambda function.

#### Parameters

##### id

`string`

construct ID

##### options

`EventSourceMappingOptions`

mapping options

#### Returns

`EventSourceMapping`

#### Inherited from

`PythonFunction.addEventSourceMapping`

***

### addFunctionUrl()

> **addFunctionUrl**(`options?`): `FunctionUrl`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:327

Adds a url to this lambda function.

#### Parameters

##### options?

`FunctionUrlOptions`

#### Returns

`FunctionUrl`

#### Inherited from

`PythonFunction.addFunctionUrl`

***

### addLayers()

> **addLayers**(...`layers`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:736

Adds one or more Lambda Layers to this Lambda function.

#### Parameters

##### layers

...`ILayerVersion`[]

the layers to be added.

#### Returns

`void`

#### Throws

if there are already 5 layers on this function, or the layer is incompatible with this function's runtime.

#### Inherited from

`PythonFunction.addLayers`

***

### addPermission()

> **addPermission**(`id`, `permission`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:285

Adds a permission to the Lambda resource policy.

#### Parameters

##### id

`string`

The id for the permission construct

##### permission

`Permission`

The permission to grant to this Lambda function.

#### Returns

`void`

#### See

Permission for details.

#### Inherited from

`PythonFunction.addPermission`

***

### addToRolePolicy()

> **addToRolePolicy**(`statement`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:289

Adds a statement to the IAM role assumed by the instance.

#### Parameters

##### statement

`PolicyStatement`

#### Returns

`void`

#### Inherited from

`PythonFunction.addToRolePolicy`

***

### applyRemovalPolicy()

> **applyRemovalPolicy**(`policy`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:147

Apply the given removal policy to this resource

The Removal Policy controls what happens to this resource when it stops
being managed by CloudFormation, either because you've removed it from the
CDK application or because you've made a change that requires the resource
to be replaced.

The resource can be deleted (`RemovalPolicy.DESTROY`), or left in your AWS
account for data recovery and cleanup later (`RemovalPolicy.RETAIN`).

#### Parameters

##### policy

`RemovalPolicy`

#### Returns

`void`

#### Inherited from

`PythonFunction.applyRemovalPolicy`

***

### configureAsyncInvoke()

> **configureAsyncInvoke**(`options`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:326

Configures options for asynchronous invocation.

#### Parameters

##### options

`EventInvokeConfigOptions`

#### Returns

`void`

#### Inherited from

`PythonFunction.configureAsyncInvoke`

***

### considerWarningOnInvokeFunctionPermissions()

> **considerWarningOnInvokeFunctionPermissions**(`scope`, `action`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:278

A warning will be added to functions under the following conditions:
- permissions that include `lambda:InvokeFunction` are added to the unqualified function.
- function.currentVersion is invoked before or after the permission is created.

This applies only to permissions on Lambda functions, not versions or aliases.
This function is overridden as a noOp for QualifiedFunctionBase.

#### Parameters

##### scope

`Construct`

##### action

`string`

#### Returns

`void`

#### Inherited from

`PythonFunction.considerWarningOnInvokeFunctionPermissions`

***

### generatePhysicalName()

> `protected` **generatePhysicalName**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:148

#### Returns

`string`

#### Inherited from

`PythonFunction.generatePhysicalName`

***

### getResourceArnAttribute()

> `protected` **getResourceArnAttribute**(`arnAttr`, `arnComponents`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:178

Returns an environment-sensitive token that should be used for the
resource's "ARN" attribute (e.g. `bucket.bucketArn`).

Normally, this token will resolve to `arnAttr`, but if the resource is
referenced across environments, `arnComponents` will be used to synthesize
a concrete ARN with the resource's physical name. Make sure to reference
`this.physicalName` in `arnComponents`.

#### Parameters

##### arnAttr

`string`

The CFN attribute which resolves to the ARN of the resource.
Commonly it will be called "Arn" (e.g. `resource.attrArn`), but sometimes
it's the CFN resource's `ref`.

##### arnComponents

`ArnComponents`

The format of the ARN of this resource. You must
reference `this.physicalName` somewhere within the ARN in order for
cross-environment references to work.

#### Returns

`string`

#### Inherited from

`PythonFunction.getResourceArnAttribute`

***

### getResourceNameAttribute()

> `protected` **getResourceNameAttribute**(`nameAttr`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:160

Returns an environment-sensitive token that should be used for the
resource's "name" attribute (e.g. `bucket.bucketName`).

Normally, this token will resolve to `nameAttr`, but if the resource is
referenced across environments, it will be resolved to `this.physicalName`,
which will be a concrete name.

#### Parameters

##### nameAttr

`string`

The CFN attribute which resolves to the resource's name.
Commonly this is the resource's `ref`.

#### Returns

`string`

#### Inherited from

`PythonFunction.getResourceNameAttribute`

***

### grantInvoke()

> **grantInvoke**(`grantee`): `Grant`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:307

Grant the given identity permissions to invoke this Lambda

#### Parameters

##### grantee

`IGrantable`

#### Returns

`Grant`

#### Inherited from

`PythonFunction.grantInvoke`

***

### grantInvokeCompositePrincipal()

> **grantInvokeCompositePrincipal**(`compositePrincipal`): `Grant`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:324

Grant multiple principals the ability to invoke this Lambda via CompositePrincipal

#### Parameters

##### compositePrincipal

`CompositePrincipal`

#### Returns

`Grant`[]

#### Inherited from

`PythonFunction.grantInvokeCompositePrincipal`

***

### grantInvokeLatestVersion()

> **grantInvokeLatestVersion**(`grantee`): `Grant`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:312

Grant the given identity permissions to invoke the $LATEST version or
unqualified version of this Lambda

#### Parameters

##### grantee

`IGrantable`

#### Returns

`Grant`

#### Inherited from

`PythonFunction.grantInvokeLatestVersion`

***

### grantInvokeUrl()

> **grantInvokeUrl**(`grantee`): `Grant`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:320

Grant the given identity permissions to invoke this Lambda Function URL

#### Parameters

##### grantee

`IGrantable`

#### Returns

`Grant`

#### Inherited from

`PythonFunction.grantInvokeUrl`

***

### grantInvokeVersion()

> **grantInvokeVersion**(`grantee`, `version`): `Grant`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:316

Grant the given identity permissions to invoke the given version of this Lambda

#### Parameters

##### grantee

`IGrantable`

##### version

`IVersion`

#### Returns

`Grant`

#### Inherited from

`PythonFunction.grantInvokeVersion`

***

### invalidateVersionBasedOn()

> **invalidateVersionBasedOn**(`x`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:728

Mix additional information into the hash of the Version object

The Lambda Function construct does its best to automatically create a new
Version when anything about the Function changes (its code, its layers,
any of the other properties).

However, you can sometimes source information from places that the CDK cannot
look into, like the deploy-time values of SSM parameters. In those cases,
the CDK would not force the creation of a new Version object when it actually
should.

This method can be used to invalidate the current Version object. Pass in
any string into this method, and make sure the string changes when you know
a new Version needs to be created.

This method may be called more than once.

#### Parameters

##### x

`string`

#### Returns

`void`

#### Inherited from

`PythonFunction.invalidateVersionBasedOn`

***

### metric()

> **metric**(`metricName`, `props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/lambda-augmentations.generated.d.ts:39

Return the given named metric for this Function

#### Parameters

##### metricName

`string`

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metric`

***

### metricDuration()

> **metricDuration**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/lambda-augmentations.generated.d.ts:63

How long execution of this Lambda takes

Average over 5 minutes

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metricDuration`

***

### metricErrors()

> **metricErrors**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/lambda-augmentations.generated.d.ts:57

How many invocations of this Lambda fail

Sum over 5 minutes

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metricErrors`

***

### metricInvocations()

> **metricInvocations**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/lambda-augmentations.generated.d.ts:51

How often this Lambda is invoked

Sum over 5 minutes

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metricInvocations`

***

### metricThrottles()

> **metricThrottles**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/lambda-augmentations.generated.d.ts:45

How often this Lambda is throttled

Sum over 5 minutes

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metricThrottles`

***

### toString()

> **toString**(): `string`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:279

Returns a string representation of this construct.

#### Returns

`string`

#### Inherited from

`PythonFunction.toString`

***

### warnInvokeFunctionPermissions()

> `protected` **warnInvokeFunctionPermissions**(`scope`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function-base.d.ts:279

#### Parameters

##### scope

`Construct`

#### Returns

`void`

#### Inherited from

`PythonFunction.warnInvokeFunctionPermissions`

***

### classifyVersionProperty()

> `static` **classifyVersionProperty**(`propertyName`, `locked`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:580

Record whether specific properties in the `AWS::Lambda::Function` resource should
also be associated to the Version resource.
See 'currentVersion' section in the module README for more details.

#### Parameters

##### propertyName

`string`

The property to classify

##### locked

`boolean`

whether the property should be associated to the version or not.

#### Returns

`void`

#### Inherited from

`PythonFunction.classifyVersionProperty`

***

### fromFunctionArn()

> `static` **fromFunctionArn**(`scope`, `id`, `functionArn`): `IFunction`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:591

Import a lambda function into the CDK using its ARN.

For `Function.addPermissions()` to work on this imported lambda, make sure that is
in the same account and region as the stack you are importing it into.

#### Parameters

##### scope

`Construct`

##### id

`string`

##### functionArn

`string`

#### Returns

`IFunction`

#### Inherited from

`PythonFunction.fromFunctionArn`

***

### fromFunctionAttributes()

> `static` **fromFunctionAttributes**(`scope`, `id`, `attrs`): `IFunction`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:603

Creates a Lambda function object which represents a function not defined
within this stack.

For `Function.addPermissions()` to work on this imported lambda, set the sameEnvironment property to true
if this imported lambda is in the same account and region as the stack you are importing it into.

#### Parameters

##### scope

`Construct`

The parent construct

##### id

`string`

The name of the lambda construct

##### attrs

`FunctionAttributes`

the attributes of the function to import

#### Returns

`IFunction`

#### Inherited from

`PythonFunction.fromFunctionAttributes`

***

### fromFunctionName()

> `static` **fromFunctionName**(`scope`, `id`, `functionName`): `IFunction`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:584

Import a lambda function into the CDK using its name

#### Parameters

##### scope

`Construct`

##### id

`string`

##### functionName

`string`

#### Returns

`IFunction`

#### Inherited from

`PythonFunction.fromFunctionName`

***

### isConstruct()

> `static` **isConstruct**(`x`): `x is Construct`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:262

Checks if `x` is a construct.

Use this method instead of `instanceof` to properly detect `Construct`
instances, even when the construct library is symlinked.

Explanation: in JavaScript, multiple copies of the `constructs` library on
disk are seen as independent, completely different libraries. As a
consequence, the class `Construct` in each copy of the `constructs` library
is seen as a different class, and an instance of one class will not test as
`instanceof` the other class. `npm install` will not create installations
like this, but users may manually symlink construct libraries together or
use a monorepo tool: in those cases, multiple copies of the `constructs`
library can be accidentally installed, and `instanceof` will behave
unpredictably. It is safest to avoid using `instanceof`, and using
this type-testing method instead.

#### Parameters

##### x

`any`

Any object

#### Returns

`x is Construct`

true if `x` is an object created from a class which extends `Construct`.

#### Inherited from

`PythonFunction.isConstruct`

***

### isOwnedResource()

> `static` **isOwnedResource**(`construct`): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:109

Returns true if the construct was created by CDK, and false otherwise

#### Parameters

##### construct

`IConstruct`

#### Returns

`boolean`

#### Inherited from

`PythonFunction.isOwnedResource`

***

### isResource()

> `static` **isResource**(`construct`): `construct is Resource`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/resource.d.ts:105

Check whether the given construct is a Resource

#### Parameters

##### construct

`IConstruct`

#### Returns

`construct is Resource`

#### Inherited from

`PythonFunction.isResource`

***

### metricAll()

> `static` **metricAll**(`metricName`, `props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:607

Return the given named metric for this Lambda

#### Parameters

##### metricName

`string`

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Inherited from

`PythonFunction.metricAll`

***

### metricAllConcurrentExecutions()

> `static` **metricAllConcurrentExecutions**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:637

Metric for the number of concurrent executions across all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
max over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllConcurrentExecutions`

***

### metricAllDuration()

> `static` **metricAllDuration**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:619

Metric for the Duration executing all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
average over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllDuration`

***

### metricAllErrors()

> `static` **metricAllErrors**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:613

Metric for the number of Errors executing all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
sum over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllErrors`

***

### metricAllInvocations()

> `static` **metricAllInvocations**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:625

Metric for the number of invocations of all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
sum over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllInvocations`

***

### metricAllThrottles()

> `static` **metricAllThrottles**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:631

Metric for the number of throttled invocations of all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
sum over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllThrottles`

***

### metricAllUnreservedConcurrentExecutions()

> `static` **metricAllUnreservedConcurrentExecutions**(`props?`): `Metric`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-lambda/lib/function.d.ts:643

Metric for the number of unreserved concurrent executions across all Lambdas

#### Parameters

##### props?

`MetricOptions`

#### Returns

`Metric`

#### Default

```ts
max over 5 minutes
```

#### Inherited from

`PythonFunction.metricAllUnreservedConcurrentExecutions`
