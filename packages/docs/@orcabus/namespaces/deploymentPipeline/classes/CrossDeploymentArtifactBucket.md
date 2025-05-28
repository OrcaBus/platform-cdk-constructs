[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CrossDeploymentArtifactBucket

# Class: CrossDeploymentArtifactBucket

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:37](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L37)

## Extends

- `Construct`

## Implements

- [`ICrossDeploymentArtifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md)

## Constructors

### Constructor

> **new CrossDeploymentArtifactBucket**(`scope`, `id`): `CrossDeploymentArtifactBucket`

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:50](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L50)

#### Parameters

##### scope

`Construct`

##### id

`string`

#### Returns

`CrossDeploymentArtifactBucket`

#### Overrides

`Construct.constructor`

## Properties

### artifactBucket

> `readonly` **artifactBucket**: `IBucket`

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:44](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L44)

The S3 bucket used to store artifacts for cross-deployment pipelines.

#### Implementation of

[`ICrossDeploymentArtifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md).[`artifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md#artifactbucket)

***

### artifactKms

> `readonly` **artifactKms**: `IKey`

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:48](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L48)

The KMS key used to encrypt artifacts for cross-deployment pipelines.

#### Implementation of

[`ICrossDeploymentArtifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md).[`artifactKms`](../interfaces/ICrossDeploymentArtifactBucket.md#artifactkms)

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

The tree node.

#### Inherited from

`Construct.node`

## Methods

### toString()

> **toString**(): `string`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:279

Returns a string representation of this construct.

#### Returns

`string`

#### Inherited from

`Construct.toString`

***

### fromLookup()

> `static` **fromLookup**(`scope`): [`ICrossDeploymentArtifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md)

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:115](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L115)

Imports an existing cross-deployment artifact bucket and its KMS key
using SSM and resource lookups.

#### Parameters

##### scope

`Construct`

The scope in which to look up the artifact bucket.

#### Returns

[`ICrossDeploymentArtifactBucket`](../interfaces/ICrossDeploymentArtifactBucket.md)

ICrossDeploymentArtifactBucket

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

`Construct.isConstruct`
