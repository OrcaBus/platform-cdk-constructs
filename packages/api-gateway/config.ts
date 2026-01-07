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
  BETA: [
    "https://orcaui.dev.umccr.org",
    "https://portal.dev.umccr.org",
    "http://localhost:3000",
  ],
  GAMMA: ["https://orcaui.stg.umccr.org", "https://portal.stg.umccr.org"],
  PROD: ["https://orcaui.umccr.org", "https://portal.umccr.org"],
};

// portal - TokenServiceStack
export const COGNITO_PORTAL_APP_CLIENT_ID_PARAMETER_NAME =
  "/data_portal/client/data2/cog_app_client_id_stage";

export const COGNITO_ORCAUI_APP_CLIENT_ID_PARAMETER_NAME =
  "/orcaui/cog_app_client_id_stage";

// localhost development
export const COGNITO_LOCAL_APP_CLIENT_ID_PARAMETER_NAME =
  "/data_portal/client/cog_app_client_id_local";

// Base client IDs used across all environments
const BASE_COGNITO_CLIENT_ID_PARAMETER_NAMES = [
  COGNITO_PORTAL_APP_CLIENT_ID_PARAMETER_NAME,
  COGNITO_ORCAUI_APP_CLIENT_ID_PARAMETER_NAME,
];

// Environment-specific client ID arrays
export const COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY: Record<
  StageName,
  string[]
> = {
  BETA: [
    ...BASE_COGNITO_CLIENT_ID_PARAMETER_NAMES,
    COGNITO_LOCAL_APP_CLIENT_ID_PARAMETER_NAME,
  ],
  GAMMA: BASE_COGNITO_CLIENT_ID_PARAMETER_NAMES,
  PROD: BASE_COGNITO_CLIENT_ID_PARAMETER_NAMES,
};

export const DEFAULT_COGNITO_USER_POOL_ID_PARAMETER_NAME =
  "/data_portal/client/cog_user_pool_id";

export const CERTIFICATE_ARN_PARAMETER_NAME = "/umccr/certificate_arn";
export const HOSTED_ZONE_DOMAIN_PARAMETER_NAME = "/hosted_zone/umccr/name";
export const HOSTED_ZONE_ID_PARAMETER_NAME = "/hosted_zone/umccr/id";

export const getDefaultApiGatewayConfiguration = (stage: StageName) => {
  return {
    cognitoClientIdParameterNameArray:
      COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY[stage],
    corsAllowOrigins: DEFAULT_ALLOW_CORS_ORIGINS[stage],
    apiGwLogsConfig: DEFAULT_LOGS_CONFIG[stage],
  };
};

/**
 * The SSM parameter name for the HTTP Lambda authorizer ARN.
 */
export const AUTH_STACK_HTTP_LAMBDA_AUTHORIZER_PARAMETER_NAME =
  "/orcabus/authorization-stack/http-lambda-authorization-arn";
