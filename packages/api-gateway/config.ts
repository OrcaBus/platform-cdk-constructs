import { RetentionDays } from "aws-cdk-lib/aws-logs";
import { RemovalPolicy } from "aws-cdk-lib";
import { StageName } from "../shared-config/accounts";

export interface LogsConfigProps {
  /**
   * Retention policy for the API Gateway logs.
   */
  readonly retention: RetentionDays;

  /**
   * Removal policy for the log group
   */
  readonly removalPolicy: RemovalPolicy;
}

export const DEFAULT_LOGS_CONFIG: Record<StageName, LogsConfigProps> = {
  BETA: {
    retention: RetentionDays.TWO_WEEKS,
    removalPolicy: RemovalPolicy.DESTROY,
  },
  GAMMA: {
    retention: RetentionDays.TWO_WEEKS,
    removalPolicy: RemovalPolicy.DESTROY,
  },
  PROD: {
    retention: RetentionDays.TWO_YEARS,
    removalPolicy: RemovalPolicy.RETAIN,
  },
};

export const DEFAULT_ALLOW_CORS_ORIGINS: Record<StageName, string[]> = {
  BETA: ["https://orcaui.dev.umccr.org"],
  GAMMA: ["https://orcaui.stg.umccr.org"],
  PROD: ["https://orcaui.prod.umccr.org", "https://orcaui.umccr.org"],
};

export const DEFAULT_COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY = [
  "/data_portal/client/data2/cog_app_client_id_stage", // portal - TokenServiceStack
  "/orcaui/cog_app_client_id_stage", // orcaui - https://github.com/umccr/orca-ui
];

export const DEFAULT_COGNITO_USER_POOL_ID_PARAMETER_NAME =
  "/data_portal/client/cog_user_pool_id";

export const CERTIFICATE_ARN_PARAMETER_NAME = "/umccr/certificate_arn";
export const HOSTED_ZONE_DOMAIN_PARAMETER_NAME = "/hosted_zone/umccr/name";
export const HOSTED_ZONE_ID_PARAMETER_NAME = "/hosted_zone/umccr/id";

export const getDefaultApiGatewayConfiguration = (stage: StageName) => {
  return {
    cognitoClientIdParameterNameArray:
      DEFAULT_COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY,
    corsAllowOrigins: DEFAULT_ALLOW_CORS_ORIGINS[stage],
    apiGwLogsConfig: DEFAULT_LOGS_CONFIG[stage],
  };
};

/**
 * The SSM parameter name for the HTTP Lambda authorizer ARN.
 */
export const AUTH_STACK_HTTP_LAMBDA_AUTHORIZER_PARAMETER_NAME =
  "/orcabus/authorization-stack/http-lambda-authorization-arn";
