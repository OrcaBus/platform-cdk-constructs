import { RetentionDays } from "aws-cdk-lib/aws-logs";
import { RemovalPolicy } from "aws-cdk-lib";
import { StageName } from "../utils";

export const DEFAULT_LOGS_CONFIG = {
  BETA: {
    retention: RetentionDays.TWO_WEEKS,
    removalPolicy: RemovalPolicy.DESTROY,
  },
  GAMMA: {
    retention: RetentionDays.TWO_WEEKS,
    removalPolicy: RemovalPolicy.DESTROY,
  },
  PROD: {
    retention: RetentionDays.TWO_WEEKS,
    removalPolicy: RemovalPolicy.DESTROY,
  },
};

export const DEFAULT_ALLOW_CORS_ORIGINS = {
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

export const getDefaultApiGatewayConfiguration = (stage: StageName) => {
  return {
    cognitoClientIdParameterNameArray:
      DEFAULT_COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY,
    corsAllowOrigins: DEFAULT_ALLOW_CORS_ORIGINS[stage],
    apiGwLogsConfig: DEFAULT_LOGS_CONFIG[stage],
  };
};
