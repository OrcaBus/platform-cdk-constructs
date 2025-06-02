import { Construct } from "constructs";
import { Role, ServicePrincipal } from "aws-cdk-lib/aws-iam";
import { Duration } from "aws-cdk-lib";

/**
 * Props for the named lambda role construct.
 */
export interface NamedLambdaRoleProps {
  /**
   * The name of the role, automatically generated if not specified.
   */
  readonly name?: string;
  /**
   * Description for the role.
   */
  readonly description?: string;
  /**
   * Specify the maximum session duration.
   */
  readonly maxSessionDuration?: Duration;
}

/**
 * A construct which represents a named role that a Lambda function can assume.
 */
export class NamedLambdaRole extends Role {
  constructor(scope: Construct, id: string, props?: NamedLambdaRoleProps) {
    super(scope, id, {
      assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
      description: props?.description ?? "Lambda execution role",
      roleName: props?.name,
      maxSessionDuration: props?.maxSessionDuration,
    });
  }
}
