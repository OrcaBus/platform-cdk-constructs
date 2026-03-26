[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [monitoredQueue](../README.md) / MonitoredQueue

# Class: MonitoredQueue

Defined in: [packages/monitored-queue/index.ts:58](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L58)

A construct that defines an SQS queue, along with a DLQ and CloudWatch alarms that can notify an
SNS topic.

## Extends

- `Construct`

## Constructors

### Constructor

> **new MonitoredQueue**(`scope`, `id`, `props`): `MonitoredQueue`

Defined in: [packages/monitored-queue/index.ts:63](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L63)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`MonitoredQueueProps`](../interfaces/MonitoredQueueProps.md)

#### Returns

`MonitoredQueue`

#### Overrides

`Construct.constructor`

## Properties

### alarm

> `readonly` **alarm**: `Alarm`

Defined in: [packages/monitored-queue/index.ts:61](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L61)

***

### deadLetterQueue

> `readonly` **deadLetterQueue**: `Queue`

Defined in: [packages/monitored-queue/index.ts:60](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L60)

***

### node

> `readonly` **node**: `Node`

Defined in: node\_modules/.pnpm/constructs@10.6.0/node\_modules/constructs/lib/construct.d.ts:289

The tree node.

#### Inherited from

`Construct.node`

***

### queue

> `readonly` **queue**: `Queue`

Defined in: [packages/monitored-queue/index.ts:59](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L59)

## Accessors

### queueArn

#### Get Signature

> **get** **queueArn**(): `string`

Defined in: [packages/monitored-queue/index.ts:125](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L125)

Get the SQS queue ARN.

##### Returns

`string`

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
