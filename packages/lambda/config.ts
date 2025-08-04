import {ACCOUNT_ID_ALIAS, REGION, StageName} from "../shared-config/accounts";

export const DEFAULT_ORCABUS_TOKEN_SECRET_ID =  'orcabus/token-service-jwt'
export const DEFAULT_HOSTNAME_SSM_PARAMETER = '/hosted_zone/umccr/name'


export const MART_ENV_VARS = {
    athenaWorkgroupName: 'orcahouse',
    athenaDatasourceName: 'orcavault',
    athenaDatabaseName: 'mart'
}

export const MART_S3_BUCKET: Record<StageName, string> = {
    BETA: `data-sharing-artifacts-${ACCOUNT_ID_ALIAS.BETA}-${REGION}`,
    GAMMA: `data-sharing-artifacts-${ACCOUNT_ID_ALIAS.GAMMA}-${REGION}`,
    PROD: `data-sharing-artifacts-${ACCOUNT_ID_ALIAS.PROD}-${REGION}`
}
export const MART_S3_PREFIX = 'athena-query-results/'
export const MART_LAMBDA_FUNCTION_NAME = 'orcavault'

