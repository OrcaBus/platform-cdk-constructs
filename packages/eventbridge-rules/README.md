# EventBridge Rules

## SfnSlackNotification

This CDK construct sends Slack notifications when your Step Functions state machine changes status.

### Example

```typescript
new SfnSlackNotification(this, "SfnSlackNotification", {
  stateMachine: myDev,
  eventStatus: [SfnEventStatus.SUCCEEDED],
  title: `JOB-A: ${EventField.fromPath("$.detail.input.jobId")}`,
  message: [
    "*Execution Details:*",
    `• ARN: ${EventField.fromPath("$.detail.executionArn")}`,
    `• Status: ${EventField.fromPath("$.detail.status")}`,
  ],
  showExecutionLink: true,
});
```

### Notes

- Use `EventField.fromPath("$.jsonpath")` to include dynamic event data in your title or message.
- `showExecutionLink` adds a link to the AWS Console for the execution.
