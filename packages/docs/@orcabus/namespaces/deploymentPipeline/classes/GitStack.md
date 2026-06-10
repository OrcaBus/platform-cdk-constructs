[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / GitStack

# Class: GitStack

Defined in: [packages/deployment-stack-pipeline/stack.ts:9](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/stack.ts#L9)

Extends cdk.Stack with a CfnOutput GitCommitId
Allows us to see which version of a stack is currently deployed into an environment

## Extends

- `Stack`

## Constructors

### Constructor

> **new GitStack**(`scope`, `id`, `props?`): `GitStack`

Defined in: [packages/deployment-stack-pipeline/stack.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/stack.ts#L11)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props?

`StackProps`

#### Returns

`GitStack`

#### Overrides

`cdk.Stack.constructor`

## Properties

### \_crossRegionReferences

> `readonly` **\_crossRegionReferences**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:299

**`Internal`**

Whether cross region references are enabled for this stack

#### Inherited from

`cdk.Stack._crossRegionReferences`

***

### \_notificationArns?

> `readonly` `optional` **\_notificationArns?**: `string`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:305

**`Internal`**

SNS Notification ARNs to receive stack events.

#### Inherited from

`cdk.Stack._notificationArns`

***

### \_versionReportingEnabled

> `readonly` **\_versionReportingEnabled**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:293

**`Internal`**

Whether version reporting is enabled for this stack

Controls whether the CDK Metadata resource is injected

#### Inherited from

`cdk.Stack._versionReportingEnabled`

***

### account

> `readonly` **account**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:244

The AWS account into which this stack will be deployed.

This value is resolved according to the following rules:

1. The value provided to `env.account` when the stack is defined. This can
   either be a concrete account (e.g. `585695031111`) or the
   `Aws.ACCOUNT_ID` token.
3. `Aws.ACCOUNT_ID`, which represents the CloudFormation intrinsic reference
   `{ "Ref": "AWS::AccountId" }` encoded as a string token.

Preferably, you should use the return value as an opaque string and not
attempt to parse it to implement your logic. If you do, you must first
check that it is a concrete value an not an unresolved token. If this
value is an unresolved token (`Token.isUnresolved(stack.account)` returns
`true`), this implies that the user wishes that this stack will synthesize
into an **account-agnostic template**. In this case, your code should either
fail (throw an error, emit a synth error using `Annotations.of(construct).addError()`) or
implement some other account-agnostic behavior.

#### Inherited from

`cdk.Stack.account`

***

### artifactId

> `readonly` **artifactId**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:280

The ID of the cloud assembly artifact for this stack.

#### Inherited from

`cdk.Stack.artifactId`

***

### environment

> `readonly` **environment**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:258

The environment coordinates in which this stack is deployed. In the form
`aws://account/region`. Use `stack.account` and `stack.region` to obtain
the specific values, no need to parse.

You can use this value to determine if two stacks are targeting the same
environment.

If either `stack.account` or `stack.region` are not concrete values (e.g.
`Aws.ACCOUNT_ID` or `Aws.REGION`) the special strings `unknown-account` and/or
`unknown-region` will be used respectively to indicate this stack is
region/account-agnostic.

#### Inherited from

`cdk.Stack.environment`

***

### nestedStackResource?

> `readonly` `optional` **nestedStackResource?**: `CfnResource`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:269

If this is a nested stack, this represents its `AWS::CloudFormation::Stack`
resource. `undefined` for top-level (non-nested) stacks.

#### Inherited from

`cdk.Stack.nestedStackResource`

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:289

The tree node.

#### Inherited from

`cdk.Stack.node`

***

### region

> `readonly` **region**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:223

The AWS region into which this stack will be deployed (e.g. `us-west-2`).

This value is resolved according to the following rules:

1. The value provided to `env.region` when the stack is defined. This can
   either be a concrete region (e.g. `us-west-2`) or the `Aws.REGION`
   token.
3. `Aws.REGION`, which is represents the CloudFormation intrinsic reference
   `{ "Ref": "AWS::Region" }` encoded as a string token.

Preferably, you should use the return value as an opaque string and not
attempt to parse it to implement your logic. If you do, you must first
check that it is a concrete value an not an unresolved token. If this
value is an unresolved token (`Token.isUnresolved(stack.region)` returns
`true`), this implies that the user wishes that this stack will synthesize
into a **region-agnostic template**. In this case, your code should either
fail (throw an error, emit a synth error using `Annotations.of(construct).addError()`) or
implement some other region-agnostic behavior.

#### Inherited from

`cdk.Stack.region`

***

### synthesizer

> `readonly` **synthesizer**: `IStackSynthesizer`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:285

Synthesis method for this stack

#### Inherited from

`cdk.Stack.synthesizer`

***

### tags

> `readonly` **tags**: `TagManager`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:198

Tags to be applied to the stack.

#### Inherited from

`cdk.Stack.tags`

***

### templateFile

> `readonly` **templateFile**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:276

The name of the CloudFormation template file emitted to the output
directory during synthesis.

Example value: `MyStack.template.json`

#### Inherited from

`cdk.Stack.templateFile`

***

### templateOptions

> `readonly` **templateOptions**: `ITemplateOptions`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:202

Options for CloudFormation template (like version, transform, description).

#### Inherited from

`cdk.Stack.templateOptions`

## Accessors

### availabilityZones

#### Get Signature

> **get** **availabilityZones**(): `string`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:507

Returns the list of AZs that are available in the AWS environment
(account/region) associated with this stack.

If the stack is environment-agnostic (either account and/or region are
tokens), this property will return an array with 2 tokens that will resolve
at deploy-time to the first two availability zones returned from CloudFormation's
`Fn::GetAZs` intrinsic function.

If they are not available in the context, returns a set of dummy values and
reports them as missing, and let the CLI resolve them by calling EC2
`DescribeAvailabilityZones` on the target environment.

To specify a different strategy for selecting availability zones override this method.

##### Returns

`string`[]

#### Inherited from

`cdk.Stack.availabilityZones`

***

### bundlingRequired

#### Get Signature

> **get** **bundlingRequired**(): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:767

Indicates whether the stack requires bundling or not

##### Returns

`boolean`

#### Inherited from

`cdk.Stack.bundlingRequired`

***

### dependencies

#### Get Signature

> **get** **dependencies**(): `Stack`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:425

Return the stacks this stack depends on

##### Returns

`Stack`[]

#### Inherited from

`cdk.Stack.dependencies`

***

### env

#### Get Signature

> **get** **env**(): `ResourceEnvironment`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:783

The environment this Stack deploys to

##### Returns

`ResourceEnvironment`

#### Inherited from

`cdk.Stack.env`

***

### nested

#### Get Signature

> **get** **nested**(): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:462

Indicates if this is a nested stack, in which case `parentStack` will include a reference to it's parent.

##### Returns

`boolean`

#### Inherited from

`cdk.Stack.nested`

***

### nestedStackParent

#### Get Signature

> **get** **nestedStackParent**(): `Stack` \| `undefined`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:511

If this is a nested stack, returns its parent stack.

##### Returns

`Stack` \| `undefined`

#### Inherited from

`cdk.Stack.nestedStackParent`

***

### notificationArns

#### Get Signature

> **get** **notificationArns**(): `string`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:458

Returns the list of notification Amazon Resource Names (ARNs) for the current stack.

##### Returns

`string`[]

#### Inherited from

`cdk.Stack.notificationArns`

***

### partition

#### Get Signature

> **get** **partition**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:442

The partition in which this stack is defined

##### Returns

`string`

#### Inherited from

`cdk.Stack.partition`

***

### stackId

#### Get Signature

> **get** **stackId**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:454

The ID of the stack

##### Example

```ts
// After resolving, looks like
'arn:aws:cloudformation:us-west-2:123456789012:stack/teststack/51af3dc0-da77-11e4-872e-1234567db123'
```

##### Returns

`string`

#### Inherited from

`cdk.Stack.stackId`

***

### stackName

#### Get Signature

> **get** **stackName**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:438

The concrete CloudFormation physical stack name.

This is either the name defined explicitly in the `stackName` prop or
allocated based on the stack's location in the construct tree. Stacks that
are directly defined under the app use their construct `id` as their stack
name. Stacks that are defined deeper within the tree will use a hashed naming
scheme based on the construct path to ensure uniqueness.

If you wish to obtain the deploy-time AWS::StackName intrinsic,
you can use `Aws.STACK_NAME` directly.

##### Returns

`string`

#### Inherited from

`cdk.Stack.stackName`

***

### terminationProtection

#### Get Signature

> **get** **terminationProtection**(): `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:262

Whether termination protection is enabled for this stack.

##### Returns

`boolean`

#### Set Signature

> **set** **terminationProtection**(`value`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:263

##### Parameters

###### value

`boolean`

##### Returns

`void`

#### Inherited from

`cdk.Stack.terminationProtection`

***

### urlSuffix

#### Get Signature

> **get** **urlSuffix**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:446

The Amazon domain suffix for the region in which this stack is defined

##### Returns

`string`

#### Inherited from

`cdk.Stack.urlSuffix`

## Methods

### \_addAssemblyDependency()

> **\_addAssemblyDependency**(`target`, `reason?`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:543

**`Internal`**

Called implicitly by the `addDependency` helper function in order to
realize a dependency between two top-level stacks at the assembly level.

Use `stack.addDependency` to define the dependency between any two stacks,
and take into account nested stack relationships.

#### Parameters

##### target

`Stack`

##### reason?

`StackDependencyReason`

#### Returns

`void`

#### Inherited from

`cdk.Stack._addAssemblyDependency`

***

### \_obtainAssemblyDependencies()

> **\_obtainAssemblyDependencies**(`reasonFilter`): `Element`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:552

**`Internal`**

Called implicitly by the `obtainDependencies` helper function in order to
collect resource dependencies across two top-level stacks at the assembly level.

Use `stack.obtainDependencies` to see the dependencies between any two stacks.

#### Parameters

##### reasonFilter

`StackDependencyReason`

#### Returns

`Element`[]

#### Inherited from

`cdk.Stack._obtainAssemblyDependencies`

***

### \_removeAssemblyDependency()

> **\_removeAssemblyDependency**(`target`, `reasonFilter?`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:562

**`Internal`**

Called implicitly by the `removeDependency` helper function in order to
remove a dependency between two top-level stacks at the assembly level.

Use `stack.addDependency` to define the dependency between any two stacks,
and take into account nested stack relationships.

#### Parameters

##### target

`Stack`

##### reasonFilter?

`StackDependencyReason`

#### Returns

`void`

#### Inherited from

`cdk.Stack._removeAssemblyDependency`

***

### \_synthesizeTemplate()

> **\_synthesizeTemplate**(`session`, `lookupRoleArn?`, `lookupRoleExternalId?`, `lookupRoleAdditionalOptions?`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:567

**`Internal`**

Synthesizes the cloudformation template into a cloud assembly.

#### Parameters

##### session

`ISynthesisSession`

##### lookupRoleArn?

`string`

##### lookupRoleExternalId?

`string`

##### lookupRoleAdditionalOptions?

#### Returns

`void`

#### Inherited from

`cdk.Stack._synthesizeTemplate`

***

### \_toCloudFormation()

> `protected` **\_toCloudFormation**(): `any`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:713

**`Internal`**

Returns the CloudFormation template for this stack by traversing
the tree and invoking _toCloudFormation() on all Entity objects.

#### Returns

`any`

#### Inherited from

`cdk.Stack._toCloudFormation`

***

### \_validateId()

> `protected` **\_validateId**(`name`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:706

**`Internal`**

Validate stack name

CloudFormation stack names can include dashes in addition to the regular identifier
character classes, and we don't allow one of the magic markers.

#### Parameters

##### name

`string`

#### Returns

`void`

#### Inherited from

`cdk.Stack._validateId`

***

### addDependency()

> **addDependency**(`target`, `reason?`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:421

Add a dependency between this stack and another stack.

This can be used to define dependencies between any two stacks within an
app, and also supports nested stacks.

#### Parameters

##### target

`Stack`

##### reason?

`string`

#### Returns

`void`

#### Inherited from

`cdk.Stack.addDependency`

***

### addMetadata()

> **addMetadata**(`key`, `value`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:533

Adds an arbitrary key-value pair, with information you want to record about the stack.
These get translated to the Metadata section of the generated template.

#### Parameters

##### key

`string`

##### value

`any`

#### Returns

`void`

#### See

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/metadata-section-structure.html

#### Inherited from

`cdk.Stack.addMetadata`

***

### addStackTag()

> **addStackTag**(`tagName`, `tagValue`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:773

Configure a stack tag

At deploy time, CloudFormation will automatically apply all stack tags to all resources in the stack.

#### Parameters

##### tagName

`string`

##### tagValue

`string`

#### Returns

`void`

#### Inherited from

`cdk.Stack.addStackTag`

***

### addTransform()

> **addTransform**(`transform`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:526

Add a Transform to this stack. A Transform is a macro that AWS
CloudFormation uses to process your template.

Duplicate values are removed when stack is synthesized.

#### Parameters

##### transform

`string`

The transform to add

#### Returns

`void`

#### See

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-section-structure.html

#### Example

```ts
declare const stack: Stack;

stack.addTransform('AWS::Serverless-2016-10-31')
```

#### Inherited from

`cdk.Stack.addTransform`

***

### allocateLogicalId()

> `protected` **allocateLogicalId**(`cfnElement`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:697

Returns the naming scheme used to allocate logical IDs. By default, uses
the `HashedAddressingScheme` but this method can be overridden to customize
this behavior.

In order to make sure logical IDs are unique and stable, we hash the resource
construct tree path (i.e. toplevel/secondlevel/.../myresource) and add it as
a suffix to the path components joined without a separator (CloudFormation
IDs only allow alphanumeric characters).

The result will be:

  <path.join('')><md5(path.join('/')>
    "human"      "hash"

If the "human" part of the ID exceeds 240 characters, we simply trim it so
the total ID doesn't exceed CloudFormation's 255 character limit.

We only take 8 characters from the md5 hash (0.000005 chance of collision).

Special cases:

- If the path only contains a single component (i.e. it's a top-level
  resource), we won't add the hash to it. The hash is not needed for
  disambiguation and also, it allows for a more straightforward migration an
  existing CloudFormation template to a CDK stack without logical ID changes
  (or renames).
- For aesthetic reasons, if the last components of the path are the same
  (i.e. `L1/L2/Pipeline/Pipeline`), they will be de-duplicated to make the
  resulting human portion of the ID more pleasing: `L1L2Pipeline<HASH>`
  instead of `L1L2PipelinePipeline<HASH>`
- If a component is named "Default" it will be omitted from the path. This
  allows refactoring higher level abstractions around constructs without affecting
  the IDs of already deployed resources.
- If a component is named "Resource" it will be omitted from the user-visible
  path, but included in the hash. This reduces visual noise in the human readable
  part of the identifier.

#### Parameters

##### cfnElement

`CfnElement`

The element for which the logical ID is allocated.

#### Returns

`string`

#### Inherited from

`cdk.Stack.allocateLogicalId`

***

### exportStringListValue()

> **exportStringListValue**(`exportedValue`, `options?`): `string`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:656

Create a CloudFormation Export for a string list value

Returns a string list representing the corresponding `Fn.importValue()`
expression for this Export. The export expression is automatically wrapped with an
`Fn::Join` and the import value with an `Fn::Split`, since CloudFormation can only
export strings. You can control the name for the export by passing the `name` option.

If you don't supply a value for `name`, the value you're exporting must be
a Resource attribute (for example: `bucket.bucketName`) and it will be
given the same name as the automatic cross-stack reference that would be created
if you used the attribute in another Stack.

One of the uses for this method is to *remove* the relationship between
two Stacks established by automatic cross-stack references. It will
temporarily ensure that the CloudFormation Export still exists while you
remove the reference from the consuming stack. After that, you can remove
the resource and the manual export.

See `exportValue` for an example of this process.

#### Parameters

##### exportedValue

`any`

##### options?

`ExportValueOptions`

#### Returns

`string`[]

#### Inherited from

`cdk.Stack.exportStringListValue`

***

### exportValue()

> **exportValue**(`exportedValue`, `options?`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:634

Create a CloudFormation Export for a string value

Returns a string representing the corresponding `Fn.importValue()`
expression for this Export. You can control the name for the export by
passing the `name` option.

If you don't supply a value for `name`, the value you're exporting must be
a Resource attribute (for example: `bucket.bucketName`) and it will be
given the same name as the automatic cross-stack reference that would be created
if you used the attribute in another Stack.

One of the uses for this method is to *remove* the relationship between
two Stacks established by automatic cross-stack references. It will
temporarily ensure that the CloudFormation Export still exists while you
remove the reference from the consuming stack. After that, you can remove
the resource and the manual export.

Here is how the process works. Let's say there are two stacks,
`producerStack` and `consumerStack`, and `producerStack` has a bucket
called `bucket`, which is referenced by `consumerStack` (perhaps because
an AWS Lambda Function writes into it, or something like that).

It is not safe to remove `producerStack.bucket` because as the bucket is being
deleted, `consumerStack` might still be using it.

Instead, the process takes two deployments:

**Deployment 1: break the relationship**:

- Make sure `consumerStack` no longer references `bucket.bucketName` (maybe the consumer
  stack now uses its own bucket, or it writes to an AWS DynamoDB table, or maybe you just
  remove the Lambda Function altogether).
- In the `ProducerStack` class, call `this.exportValue(this.bucket.bucketName)`. This
  will make sure the CloudFormation Export continues to exist while the relationship
  between the two stacks is being broken.
- Deploy (this will effectively only change the `consumerStack`, but it's safe to deploy both).

**Deployment 2: remove the bucket resource**:

- You are now free to remove the `bucket` resource from `producerStack`.
- Don't forget to remove the `exportValue()` call as well.
- Deploy again (this time only the `producerStack` will be changed -- the bucket will be deleted).

#### Parameters

##### exportedValue

`any`

##### options?

`ExportValueOptions`

#### Returns

`string`

#### Inherited from

`cdk.Stack.exportValue`

***

### formatArn()

> **formatArn**(`components`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:480

Creates an ARN from components.

If `partition`, `region` or `account` are not specified, the stack's
partition, region and account will be used.

If any component is the empty string, an empty string will be inserted
into the generated ARN at the location that component corresponds to.

The ARN will be formatted as follows:

  arn:{partition}:{service}:{region}:{account}:{resource}{sep}{resource-name}

The required ARN pieces that are omitted will be taken from the stack that
the 'scope' is attached to. If all ARN pieces are supplied, the supplied scope
can be 'undefined'.

#### Parameters

##### components

`ArnComponents`

#### Returns

`string`

#### Inherited from

`cdk.Stack.formatArn`

***

### getLogicalId()

> **getLogicalId**(`element`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:414

Allocates a stack-unique CloudFormation-compatible logical identity for a
specific resource.

This method is called when a `CfnElement` is created and used to render the
initial logical identity of resources. Logical ID renames are applied at
this stage.

This method uses the protected method `allocateLogicalId` to render the
logical ID for an element. To modify the naming scheme, extend the `Stack`
class and override this method.

#### Parameters

##### element

`CfnElement`

The CloudFormation element for which a logical identity is
needed.

#### Returns

`string`

#### Inherited from

`cdk.Stack.getLogicalId`

***

### regionalFact()

> **regionalFact**(`factName`, `defaultValue?`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:589

Look up a fact value for the given fact for the region of this stack

Will return a definite value only if the region of the current stack is resolved.
If not, a lookup map will be added to the stack and the lookup will be done at
CDK deployment time.

What regions will be included in the lookup map is controlled by the
`@aws-cdk/core:target-partitions` context value: it must be set to a list
of partitions, and only regions from the given partitions will be included.
If no such context key is set, all regions will be included.

This function is intended to be used by construct library authors. Application
builders can rely on the abstractions offered by construct libraries and do
not have to worry about regional facts.

If `defaultValue` is not given, it is an error if the fact is unknown for
the given region.

#### Parameters

##### factName

`string`

##### defaultValue?

`string`

#### Returns

`string`

#### Inherited from

`cdk.Stack.regionalFact`

***

### removeStackTag()

> **removeStackTag**(`tagName`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:779

Remove a stack tag

At deploy time, CloudFormation will automatically apply all stack tags to all resources in the stack.

#### Parameters

##### tagName

`string`

#### Returns

`void`

#### Inherited from

`cdk.Stack.removeStackTag`

***

### renameLogicalId()

> **renameLogicalId**(`oldId`, `newId`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:398

Rename a generated logical identities

To modify the naming scheme strategy, extend the `Stack` class and
override the `allocateLogicalId` method.

#### Parameters

##### oldId

`string`

##### newId

`string`

#### Returns

`void`

#### Inherited from

`cdk.Stack.renameLogicalId`

***

### reportMissingContextKey()

> **reportMissingContextKey**(`report`): `void`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:391

Indicate that a context key was expected

Contains instructions which will be emitted into the cloud assembly on how
the key should be supplied.

#### Parameters

##### report

`MissingContext`

The set of parameters needed to obtain the context

#### Returns

`void`

#### Inherited from

`cdk.Stack.reportMissingContextKey`

***

### resolve()

> **resolve**(`obj`): `any`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:374

Resolve a tokenized value in the context of the current stack.

#### Parameters

##### obj

`any`

#### Returns

`any`

#### Inherited from

`cdk.Stack.resolve`

***

### splitArn()

> **splitArn**(`arn`, `arnFormat`): `ArnComponents`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:491

Splits the provided ARN into its components.
Works both if 'arn' is a string like 'arn:aws:s3:::bucket',
and a Token representing a dynamic CloudFormation expression
(in which case the returned components will also be dynamic CloudFormation expressions,
encoded as Tokens).

#### Parameters

##### arn

`string`

the ARN to split into its components

##### arnFormat

`ArnFormat`

the expected format of 'arn' - depends on what format the service 'arn' represents uses

#### Returns

`ArnComponents`

#### Inherited from

`cdk.Stack.splitArn`

***

### toJsonString()

> **toJsonString**(`this`, `obj`, `space?`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:378

Convert an object, potentially containing tokens, to a JSON string

#### Parameters

##### this

`void`

##### obj

`any`

##### space?

`number`

#### Returns

`string`

#### Inherited from

`cdk.Stack.toJsonString`

***

### toString()

> **toString**(): `string`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:314

Returns a string representation of this construct.

#### Returns

`string`

#### Inherited from

`cdk.Stack.toString`

***

### toYamlString()

> **toYamlString**(`obj`): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:382

Convert an object, potentially containing tokens, to a YAML string

#### Parameters

##### obj

`any`

#### Returns

`string`

#### Inherited from

`cdk.Stack.toYamlString`

***

### with()

> **with**(...`mixins`): `IConstruct`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:310

Applies one or more mixins to this construct.

Mixins are applied in order. The list of constructs is captured at the
start of the call, so constructs added by a mixin will not be visited.
Use multiple `with()` calls if subsequent mixins should apply to added
constructs.

#### Parameters

##### mixins

...`IMixin`[]

The mixins to apply

#### Returns

`IConstruct`

This construct for chaining

#### Inherited from

`cdk.Stack.with`

***

### isConstruct()

> `static` **isConstruct**(`x`): `x is Construct`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:285

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

`cdk.Stack.isConstruct`

***

### isStack()

> `static` **isStack**(`this`, `x`): `x is Stack`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:186

Return whether the given object is a Stack.

We do attribute detection since we can't reliably use 'instanceof'.

#### Parameters

##### this

`void`

##### x

`any`

#### Returns

`x is Stack`

#### Inherited from

`cdk.Stack.isStack`

***

### of()

> `static` **of**(`construct`): `Stack`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.244.0\_constructs@10.6.0/node\_modules/aws-cdk-lib/core/lib/stack.d.ts:194

Looks up the first stack scope in which `construct` is defined. Fails if there is no stack up the tree.

Will return the closest containing `Stack` or `NestedStack`.

#### Parameters

##### construct

`IConstruct`

The construct to start the search from.

#### Returns

`Stack`

#### Inherited from

`cdk.Stack.of`
