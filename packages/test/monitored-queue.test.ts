import * as cdk from "aws-cdk-lib";
import { Match, Template } from "aws-cdk-lib/assertions";
import { MonitoredQueue } from "../monitored-queue";

let stack: cdk.Stack;

beforeEach(() => {
  stack = new cdk.Stack();
});

test("Test monitored queue created props", () => {
  new MonitoredQueue(stack, "MonitoredQueue", {
    queueProps: {
      queueName: "queue",
    },
    dlqProps: {
      queueName: "queue-dlq",
    },
    snsTopicArn: "arn:aws:sns:ap-southeast-2:123456789012:topic",
  });
  const template = Template.fromStack(stack);

  template.resourceCountIs("AWS::SQS::Queue", 2);
  template.hasResourceProperties("AWS::SQS::Queue", {
    QueueName: "queue",
    RedrivePolicy: {
      deadLetterTargetArn: Match.anyValue(),
      maxReceiveCount: 3,
    },
  });
  template.hasResourceProperties("AWS::SQS::Queue", {
    QueueName: "queue-dlq",
  });
  template.hasResourceProperties("AWS::CloudWatch::Alarm", {
    ComparisonOperator: "GreaterThanThreshold",
    EvaluationPeriods: 1,
    Threshold: 0,
    AlarmActions: ["arn:aws:sns:ap-southeast-2:123456789012:topic"],
  });
});
