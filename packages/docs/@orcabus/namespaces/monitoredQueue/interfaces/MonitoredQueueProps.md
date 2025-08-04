[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [monitoredQueue](../README.md) / MonitoredQueueProps

# Interface: MonitoredQueueProps

Defined in: [packages/monitored-queue/index.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L11)

Properties for the monitored queue.

## Properties

### dlqProps?

> `readonly` `optional` **dlqProps**: [`QueueProps`](QueueProps.md)

Defined in: [packages/monitored-queue/index.ts:19](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L19)

The props for the dead-letter SQS queue when a message fails.

***

### maxReceiveCount?

> `readonly` `optional` **maxReceiveCount**: `number`

Defined in: [packages/monitored-queue/index.ts:24](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L24)

The maximum number of times a message can be unsuccessfully received before
pushing it to the DLQ. Defaults to 3.

***

### queueProps?

> `readonly` `optional` **queueProps**: [`QueueProps`](QueueProps.md)

Defined in: [packages/monitored-queue/index.ts:15](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L15)

The props for the main SQS queue.

***

### snsTopicArn?

> `readonly` `optional` **snsTopicArn**: `string`

Defined in: [packages/monitored-queue/index.ts:28](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L28)

Send the alarm notification to the SNS topic with the ARN.
