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

Defined in: node\_modules/.pnpm/constructs@10.4.2/node\_modules/constructs/lib/construct.d.ts:266

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

Defined in: [packages/monitored-queue/index.ts:117](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L117)

Get the SQS queue ARN.

##### Returns

`string`

## Methods

### alarmOldestMessage()

> **alarmOldestMessage**(`queue`, `queueProps?`): `void`

Defined in: [packages/monitored-queue/index.ts:100](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L100)

Create an alarm based on the oldest message in the queue.

#### Parameters

##### queue

`IQueue`

##### queueProps?

[`QueueProps`](../interfaces/QueueProps.md)

#### Returns

`void`

***

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
