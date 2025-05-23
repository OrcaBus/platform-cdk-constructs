[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [dynamodb](../README.md) / DynamoDbNonPartitionedConstruct

# Class: DynamoDbNonPartitionedConstruct

Defined in: [packages/dynamodb/index.ts:64](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/dynamodb/index.ts#L64)

## Extends

- `Construct`

## Constructors

### Constructor

> **new DynamoDbNonPartitionedConstruct**(`scope`, `id`, `props`): `DynamoDbNonPartitionedConstruct`

Defined in: [packages/dynamodb/index.ts:66](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/dynamodb/index.ts#L66)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`DynamoDbNonPartitionedConstructProps`](../interfaces/DynamoDbNonPartitionedConstructProps.md)

#### Returns

`DynamoDbNonPartitionedConstruct`

#### Overrides

`Construct.constructor`

## Properties

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

The tree node.

#### Inherited from

`Construct.node`

***

### table

> `readonly` **table**: `TableV2`

Defined in: [packages/dynamodb/index.ts:65](https://github.com/OrcaBus/platform-cdk-constructs/blob/342fbc450bcf042009fcb0577341af4e80a50756/packages/dynamodb/index.ts#L65)

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
