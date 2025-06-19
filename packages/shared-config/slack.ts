import { Arn, Stack } from "aws-cdk-lib";

/**
 * The SNS topic for slack alerts to alerts-dev, alerts-stg, or alerts-prod.
 */
export const SLACK_ALERTS_SNS_TOPIC = "AwsChatBotTopic-alerts";

/**
 * A helper class to construct the arn for the slack SNS topic.
 */
export class SlackAlerts {
  /**
   * Format the ARN for the slack alerts SNS topic for the current stack.
   * @param stack
   * @returns Arn
   */
  public static formatArn(stack: Stack): Arn {
    return Arn.format(
      {
        service: "sns",
        resource: SLACK_ALERTS_SNS_TOPIC,
      },
      stack,
    );
  }
}
