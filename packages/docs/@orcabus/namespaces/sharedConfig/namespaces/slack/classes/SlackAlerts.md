[**@orcabus/platform-cdk-constructs**](../../../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../../../README.md) / [sharedConfig](../../../README.md) / [slack](../README.md) / SlackAlerts

# Class: SlackAlerts

Defined in: [packages/shared-config/slack.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/shared-config/slack.ts#L11)

A helper class to construct the arn for the slack SNS topic.

## Constructors

### Constructor

> **new SlackAlerts**(): `SlackAlerts`

#### Returns

`SlackAlerts`

## Methods

### formatArn()

> `static` **formatArn**(`stack`): `Arn`

Defined in: [packages/shared-config/slack.ts:17](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/shared-config/slack.ts#L17)

Format the ARN for the slack alerts SNS topic for the current stack.

#### Parameters

##### stack

`Stack`

#### Returns

`Arn`

Arn
