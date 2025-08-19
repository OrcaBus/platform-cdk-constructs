import {
  EventField,
  IEventBus,
  Rule,
  RuleTargetInput,
} from "aws-cdk-lib/aws-events";
import { Topic } from "aws-cdk-lib/aws-sns";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import { IStateMachine } from "aws-cdk-lib/aws-stepfunctions";
import { Construct } from "constructs";
import { SNS_ALERTS_TOPIC_ARN } from "./config";
import { SnsTopic } from "aws-cdk-lib/aws-events-targets";

export enum SfnEventStatus {
  RUNNING = "RUNNING",
  SUCCEEDED = "SUCCEEDED",
  FAILED = "FAILED",
  TIMED_OUT = "TIMED_OUT",
  ABORTED = "ABORTED",
}

export interface SfnSlackNotificationProps {
  /**
   * The step function state machine to listen to.
   */
  readonly stateMachine: IStateMachine;
  /**
   * The event bus to associate with this rule.
   */
  readonly eventBus?: IEventBus;
  /**
   * The event statuses to listen for.
   */
  readonly eventStatus: SfnEventStatus[];
  /**
   * The title for the Slack notification.
   *
   * Can include dynamic content from the event payload using JSONPath expressions.
   * To reference event fields, you must use `EventField.fromPath`, e.g.,
   * `Job-alpha: ${EventField.fromPath("$.detail.input.destinationId")}`.
   * The `EventField` import is required from `aws-cdk-lib/aws-events`.
   */
  readonly title: string;
  /**
   * The detailed message content for the Slack notification.
   *
   * Each array element represents a separate line in the message.
   * Supports Slack's message formatting syntax:
   * https://api.slack.com/reference/surfaces/formatting
   *
   * **Dynamic Content:**
   * To include dynamic event data, embed JSONPath expressions in strings using `EventField.fromPath`.
   * For example, `EventField.fromPath("$.detail.executionArn")` references the `executionArn` field from the event payload.
   * The `EventField` is imported from `aws-cdk-lib/aws-events`.
   *
   * @example
   * ```typescript
   * message: [
   *   "*Execution Details:*",
   *   `• ARN: ${EventField.fromPath("$.detail.executionArn")}`,
   *   `• Status: ${EventField.fromPath("$.detail.status")}`,
   *   "",
   * ]
   * ```
   */
  readonly message: string[];
  /**
   * Whether to include a link to the Step Function execution in the Slack notification. on the first line
   *
   * Append execution arn with `https://console.aws.amazon.com/states/home?#/v2/executions/details/
   *
   * Ref: https://stackoverflow.com/a/76008805
   */
  readonly showExecutionLink?: boolean;
}

export class SfnSlackNotification extends Construct {
  public readonly rule: Rule;
  constructor(scope: Construct, id: string, props: SfnSlackNotificationProps) {
    super(scope, id);

    this.rule = new Rule(this, "SfnSlackNotificationRule", {
      eventBus: props.eventBus,
      description: `Slack notification for Step Function state machine `,
      eventPattern: {
        source: ["aws.states"],
        detailType: ["Step Functions Execution Status Change"],
        detail: {
          stateMachineArn: [props.stateMachine.stateMachineArn],
          status: props.eventStatus,
        },
      },
    });

    // get SNS topic ARN from SSM Parameter Store
    const slackTopicArn = StringParameter.valueForStringParameter(
      this,
      SNS_ALERTS_TOPIC_ARN,
    );

    const slackSnsTopic = Topic.fromTopicArn(
      this,
      "SlackAlertTopic",
      slackTopicArn,
    );
    this.rule.addTarget(
      new SnsTopic(slackSnsTopic, {
        message: RuleTargetInput.fromObject({
          version: "1.0",
          source: "custom",
          content: {
            textType: "client-markdown",
            title: props.title,
            description: [
              props.showExecutionLink
                ? `<https://console.aws.amazon.com/states/home?#/v2/executions/details/${EventField.fromPath(
                    "$.detail.executionArn",
                  )}|View in Console>`
                : "",
              ...props.message,
            ].join("\n"),
          },
        }),
      }),
    );
  }
}
