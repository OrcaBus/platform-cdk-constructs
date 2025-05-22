[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DeploymentStage

# Class: DeploymentStage

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:259](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/deployment-stack-pipeline/pipeline.ts#L259)

## Extends

- `Stage`

## Constructors

### Constructor

> **new DeploymentStage**(`scope`, `environmentName`, `env`, `stackName`, `stackClass`, `appStackProps`, `githubRepo`, `githubBranch?`): `DeploymentStage`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:260](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/deployment-stack-pipeline/pipeline.ts#L260)

#### Parameters

##### scope

`Construct`

##### environmentName

`string`

##### env

`Environment`

##### stackName

`string`

##### stackClass

(`scope`, `id`, `props`) => `Stack`

##### appStackProps

`any`

##### githubRepo

`string`

##### githubBranch?

`string`

#### Returns

`DeploymentStage`

#### Overrides

`Stage.constructor`

## Properties

### \_assemblyBuilder

> `readonly` **\_assemblyBuilder**: `CloudAssemblyBuilder`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:126

**`Internal`**

The cloud assembly builder that is being used for this App

#### Inherited from

`Stage._assemblyBuilder`

***

### account?

> `readonly` `optional` **account**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:120

The default account for all resources defined within this stage.

#### Inherited from

`Stage.account`

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

The tree node.

#### Inherited from

`Stage.node`

***

### parentStage?

> `readonly` `optional` **parentStage**: `Stage`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:137

The parent stage or `undefined` if this is the app.
*

#### Inherited from

`Stage.parentStage`

***

### policyValidationBeta1

> `readonly` **policyValidationBeta1**: `IPolicyValidationPluginBeta1`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:152

Validation plugins to run during synthesis. If any plugin reports any violation,
synthesis will be interrupted and the report displayed to the user.

#### Default

```ts
- no validation plugins are used
```

#### Inherited from

`Stage.policyValidationBeta1`

***

### region?

> `readonly` `optional` **region**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:115

The default region for all resources defined within this stage.

#### Inherited from

`Stage.region`

***

### stageName

> `readonly` **stageName**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:132

The name of the stage. Based on names of the parent stages separated by
hypens.

#### Inherited from

`Stage.stageName`

## Accessors

### artifactId

#### Get Signature

> **get** **artifactId**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:168

Artifact ID of the assembly if it is a nested stage. The root stage (app)
will return an empty string.

Derived from the construct path.

##### Returns

`string`

#### Inherited from

`Stage.artifactId`

***

### assetOutdir

#### Get Signature

> **get** **assetOutdir**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:161

The cloud assembly asset output directory.

##### Returns

`string`

#### Inherited from

`Stage.assetOutdir`

***

### outdir

#### Get Signature

> **get** **outdir**(): `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:157

The cloud assembly output directory.

##### Returns

`string`

#### Inherited from

`Stage.outdir`

## Methods

### synth()

> **synth**(`options?`): `CloudAssembly`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:175

Synthesize this stage into a cloud assembly.

Once an assembly has been synthesized, it cannot be modified. Subsequent
calls will return the same assembly.

#### Parameters

##### options?

`StageSynthesisOptions`

#### Returns

`CloudAssembly`

#### Inherited from

`Stage.synth`

***

### toString()

> **toString**(): `string`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:279

Returns a string representation of this construct.

#### Returns

`string`

#### Inherited from

`Stage.toString`

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

`Stage.isConstruct`

***

### isStage()

> `static` **isStage**(`this`, `x`): `x is Stage`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:110

Test whether the given construct is a stage.

#### Parameters

##### this

`void`

##### x

`any`

#### Returns

`x is Stage`

#### Inherited from

`Stage.isStage`

***

### of()

> `static` **of**(`construct`): `undefined` \| `Stage`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/core/lib/stage.d.ts:105

Return the stage this construct is contained with, if available. If called
on a nested stage, returns its parent.

#### Parameters

##### construct

`IConstruct`

#### Returns

`undefined` \| `Stage`

#### Inherited from

`Stage.of`
