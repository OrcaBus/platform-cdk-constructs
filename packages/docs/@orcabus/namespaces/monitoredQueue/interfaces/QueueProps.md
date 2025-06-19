[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [monitoredQueue](../README.md) / QueueProps

# Interface: QueueProps

Defined in: [packages/monitored-queue/index.ts:38](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L38)

Properties for an SQS queue.

## Properties

### queueName?

> `optional` **queueName**: `string`

Defined in: [packages/monitored-queue/index.ts:42](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L42)

The name of the queue to construct. Defaults to the automatically generated name.

***

### removalPolicy?

> `optional` **removalPolicy**: `RemovalPolicy`

Defined in: [packages/monitored-queue/index.ts:50](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L50)

The removal policy of the queue.

***

### retentionPeriod?

> `optional` **retentionPeriod**: `Duration`

Defined in: [packages/monitored-queue/index.ts:46](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/monitored-queue/index.ts#L46)

How long messages stay in the queue.
