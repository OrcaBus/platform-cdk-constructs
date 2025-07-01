import { Construct } from "constructs";
import {IQueue, Queue} from "aws-cdk-lib/aws-sqs";
import { Alarm, ComparisonOperator } from "aws-cdk-lib/aws-cloudwatch";
import {Duration, Names, RemovalPolicy} from "aws-cdk-lib";
import { Topic } from "aws-cdk-lib/aws-sns";
import { SnsAction } from "aws-cdk-lib/aws-cloudwatch-actions";

/**
 * Properties for the monitored queue.
 */
export interface MonitoredQueueProps {
  /**
   * The props for the main SQS queue.
   */
  readonly queueProps?: QueueProps;
  /**
   * The props for the dead-letter SQS queue when a message fails.
   */
  readonly dlqProps?: QueueProps;
  /**
   * The maximum number of times a message can be unsuccessfully received before
   * pushing it to the DLQ. Defaults to 3.
   */
  readonly maxReceiveCount?: number;
  /**
   * Send the alarm notification to the SNS topic with the ARN.
   */
  readonly snsTopicArn?: string;
}

/**
 * Properties for an SQS queue.
 */
export interface QueueProps {
  /**
   * The name of the queue to construct. Defaults to the automatically generated name.
   */
  readonly queueName?: string;
  /**
   * How long messages stay in the queue.
   */
  readonly retentionPeriod?: Duration;
  /**
   * The removal policy of the queue.
   */
  readonly removalPolicy?: RemovalPolicy;
  /**
   * Set an alarm when the age of the oldest message in the queue exceeds the number of seconds specified.
   * Defaults to no alarm based on the oldest message.
   */
  readonly alarmOldestMessageSeconds?: number;
}

/**
 * A construct that defines an SQS queue, along with a DLQ and CloudWatch alarms that can notify an
 * SNS topic.
 */
export class MonitoredQueue extends Construct {
  readonly queue: Queue;
  readonly deadLetterQueue: Queue;
  readonly alarm: Alarm;

  constructor(scope: Construct, id: string, props: MonitoredQueueProps) {
    super(scope, id);

    this.deadLetterQueue = new Queue(this, "DeadLetterQueue", {
      enforceSSL: true,
      ...props.dlqProps,
    });
    this.alarmOldestMessage(this.deadLetterQueue, props.dlqProps);

    this.queue = new Queue(this, "Queue", {
      enforceSSL: true,
      deadLetterQueue: {
        maxReceiveCount: props.maxReceiveCount ?? 3,
        queue: this.deadLetterQueue,
      },
      ...props.queueProps,
    });
    this.alarmOldestMessage(this.queue, props.queueProps);

    this.alarm = new Alarm(this, "Alarm", {
      metric: this.deadLetterQueue.metricApproximateNumberOfMessagesVisible(),
      comparisonOperator: ComparisonOperator.GREATER_THAN_THRESHOLD,
      threshold: 0,
      evaluationPeriods: 1,
      alarmName: `${this.queue.queueName}-alarm`,
      alarmDescription: "An event has been received in the dead letter queue.",
    });

    if (props.snsTopicArn !== undefined) {
      const topic = Topic.fromTopicArn(this, "Topic", props.snsTopicArn);
      this.alarm.addAlarmAction(new SnsAction(topic));
    }
  }

  /**
   * Create an alarm based on the oldest message in the queue.
   */
  alarmOldestMessage(queue: IQueue, queueProps?: QueueProps) {
    const seconds = queueProps?.alarmOldestMessageSeconds;
    if (seconds !== undefined) {
      const uniqueId = Names.uniqueResourceName(this, {
        maxLength: 6,
      });
      new Alarm(this, `AlarmOldestMessage-${queueProps?.queueName}-${uniqueId}`, {
        metric: queue.metricApproximateAgeOfOldestMessage(),
        comparisonOperator: ComparisonOperator.GREATER_THAN_THRESHOLD,
        threshold: seconds,
        evaluationPeriods: 1,
        alarmName: `${queue.queueName}-oldest-message-alarm`,
        alarmDescription: `The age of the oldest message has exceeded ${seconds} seconds.`,
      });
    }
  }

  /**
   * Get the SQS queue ARN.
   */
  get queueArn(): string {
    return this.queue.queueArn;
  }
}
