[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [monitoredQueue](../README.md) / MonitoredQueueProps

# Interface: MonitoredQueueProps

Defined in: [packages/monitored-queue/index.ts:15](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L15)

Properties for the monitored queue.

## Properties

### dlqProps?

> `optional` **dlqProps**: [`QueueProps`](QueueProps.md)

Defined in: [packages/monitored-queue/index.ts:23](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L23)

The props for the dead-letter SQS queue when a message fails.

***

### maxReceiveCount?

> `optional` **maxReceiveCount**: `number`

Defined in: [packages/monitored-queue/index.ts:28](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L28)

The maximum number of times a message can be unsuccessfully received before
pushing it to the DLQ. Defaults to 3.

***

### queueProps?

> `optional` **queueProps**: [`QueueProps`](QueueProps.md)

Defined in: [packages/monitored-queue/index.ts:19](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L19)

The props for the main SQS queue.

***

### snsTopicArn?

> `optional` **snsTopicArn**: `string`

Defined in: [packages/monitored-queue/index.ts:32](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L32)

Send the alarm notification to the SNS topic with the ARN.
