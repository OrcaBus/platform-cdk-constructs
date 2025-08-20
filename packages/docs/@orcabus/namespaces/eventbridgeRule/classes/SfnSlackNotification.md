[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [eventbridgeRule](../README.md) / SfnSlackNotification

# Class: SfnSlackNotification

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:79](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L79)

## Extends

- `Construct`

## Constructors

### Constructor

> **new SfnSlackNotification**(`scope`, `id`, `props`): `SfnSlackNotification`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:81](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L81)

#### Parameters

##### scope

`Construct`

##### id

`string`

##### props

[`SfnSlackNotificationProps`](../interfaces/SfnSlackNotificationProps.md)

#### Returns

`SfnSlackNotification`

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

### rule

> `readonly` **rule**: `Rule`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:80](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L80)

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
