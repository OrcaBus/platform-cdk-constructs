[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [eventbridgeRule](../README.md) / SfnSlackNotificationProps

# Interface: SfnSlackNotificationProps

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:22](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L22)

## Properties

### eventBus?

> `readonly` `optional` **eventBus**: `IEventBus`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:32](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L32)

The event statuses to listen for.

 Default: The default AWS event bus

***

### eventStatus

> `readonly` **eventStatus**: [`SfnEventStatus`](../enumerations/SfnEventStatus.md)[]

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:36](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L36)

The event statuses to listen for.

***

### message

> `readonly` **message**: `string`[]

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:69](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L69)

The detailed message content for the Slack notification.

Each array element represents a separate line in the message.
Supports Slack's message formatting syntax:
https://api.slack.com/reference/surfaces/formatting

**Dynamic Content:**
To include dynamic event data, embed JSONPath expressions in strings using `EventField.fromPath`.
For example, `EventField.fromPath("$.detail.executionArn")` references the `executionArn` field from the event payload.
The `EventField` is imported from `aws-cdk-lib/aws-events`.

Example:

```typescript
message: [
  "*Execution Details:*",
  `• ARN: ${EventField.fromPath("$.detail.executionArn")}`,
  `• Status: ${EventField.fromPath("$.detail.status")}`,
  "",
]
```

***

### showExecutionLink?

> `readonly` `optional` **showExecutionLink**: `boolean`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:77](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L77)

Whether to include a link to the Step Function execution in the Slack notification. on the first line

Append execution arn with `https://console.aws.amazon.com/states/home?#/v2/executions/details/

Ref: https://stackoverflow.com/a/76008805

***

### stateMachine

> `readonly` **stateMachine**: `IStateMachine`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:26](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L26)

The step function state machine to listen to.

***

### title

> `readonly` **title**: `string`

Defined in: [packages/eventbridge-rules/sfn-slack-notification.ts:45](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/eventbridge-rules/sfn-slack-notification.ts#L45)

The title for the Slack notification.

Can include dynamic content from the event payload using JSONPath expressions.
To reference event fields, you must use `EventField.fromPath`, e.g.,
`Job-alpha: ${EventField.fromPath("$.detail.input.destinationId")}`.
The `EventField` import is required from `aws-cdk-lib/aws-events`.
