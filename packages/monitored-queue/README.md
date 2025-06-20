# MonitoredQueue

A construct creating an SQS queue that has an attached dead-letter queue and an alarm that triggers when a message
arrives in the dead-letter queue. An SNS topic can also be notified when the alarm triggers.

Usage example:

```ts
new MonitoredQueue(this, "MonitoredQueue", {
  queueProps: {
    queueName: "queue",
    removalPolicy: RemovalPolicy.RETAIN,
  },
  dlqProps: {
    queueName: `$queue-dlq`,
    removalPolicy: RemovalPolicy.RETAIN,
    retentionPeriod: Duration.days(14),
  },
  snsTopicArn: SlackAlerts.formatArn(this),
});
```
