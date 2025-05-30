[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [provider](../README.md) / ProviderFunction

# Class: ProviderFunction

Defined in: [packages/provider-function/index.ts:41](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/provider-function/index.ts#L41)

A construct for invoking a Lambda function using the CDK provider framework:
https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html#provider-framework.

This is useful for performing database actions such as migrations during CloudFormation stack creation, where CDK
deployment will fail if the function fails. To use this construct the Lambda function must return values according
to the provider framework.

## Extends

- `Construct`

## Constructors

### Constructor

> **new ProviderFunction**(`scope`, `id`, `props`): `ProviderFunction`

Defined in: [packages/provider-function/index.ts:45](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/provider-function/index.ts#L45)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`ProviderFunctionProps`](../interfaces/ProviderFunctionProps.md)

#### Returns

`ProviderFunction`

#### Overrides

`Construct.constructor`

## Properties

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

The tree node.

#### Inherited from

`Construct.node`

## Accessors

### function

#### Get Signature

> **get** **function**(): `IFunction`

Defined in: [packages/provider-function/index.ts:82](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/provider-function/index.ts#L82)

Get the function.

##### Returns

`IFunction`

***

### response

#### Get Signature

> **get** **response**(): `string`

Defined in: [packages/provider-function/index.ts:75](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/provider-function/index.ts#L75)

Get the response of the Lambda function.

##### Returns

`string`

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
