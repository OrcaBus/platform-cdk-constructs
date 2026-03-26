[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [apigateway](../README.md) / OrcaBusApiGateway

# Class: OrcaBusApiGateway

Defined in: [packages/api-gateway/api-gateway.ts:72](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L72)

## Extends

- `Construct`

## Constructors

### Constructor

> **new OrcaBusApiGateway**(`scope`, `id`, `props`): `OrcaBusApiGateway`

Defined in: [packages/api-gateway/api-gateway.ts:94](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L94)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`OrcaBusApiGatewayProps`](../interfaces/OrcaBusApiGatewayProps.md)

#### Returns

`OrcaBusApiGateway`

#### Overrides

`Construct.constructor`

## Properties

### authStackHttpLambdaAuthorizer

> `readonly` **authStackHttpLambdaAuthorizer**: `HttpLambdaAuthorizer`

Defined in: [packages/api-gateway/api-gateway.ts:92](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L92)

The Lambda HTTP Authorizer used to enforce authorization policies
defined in the authorization stack.

To use this, set it as the `authorizer` property in an `HttpRoute` construct.
Example: `authorizer: apiGateway.authStackHttpLambdaAuthorizer`

***

### domainName

> `readonly` **domainName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:84](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L84)

Domain name defined in this gateway

***

### httpApi

> `readonly` **httpApi**: `HttpApi`

Defined in: [packages/api-gateway/api-gateway.ts:80](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L80)

The HTTP API

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:289

The tree node.

#### Inherited from

`Construct.node`

***

### region

> `readonly` **region**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:76](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L76)

The AWS region where the API Gateway is deployed.

## Methods

### toString()

> **toString**(): `string`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:314

Returns a string representation of this construct.

#### Returns

`string`

#### Inherited from

`Construct.toString`

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

`Construct.with`

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

`Construct.isConstruct`
