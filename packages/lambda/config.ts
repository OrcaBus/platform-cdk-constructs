import {accountIdAlias, REGION, StageName} from "../shared-config/accounts";

export const DEFAULT_ORCABUS_TOKEN_SECRET_ID =  'orcabus/token-service-jwt'
export const DEFAULT_HOSTNAME_SSM_PARAMETER = '/hosted_zone/umccr/name'


export const MART_ENV_VARS = {
    athenaWorkgroupName: 'orcahouse',
    athenaDatasourceName: 'orcavault',
    athenaDatabaseName: 'mart'
}

export const MART_S3_BUCKET: Record<StageName, string> = {
    BETA: `data-sharing-artifacts-${accountIdAlias.BETA}-${REGION}`,
    GAMMA: `data-sharing-artifacts-${accountIdAlias.GAMMA}-${REGION}`,
    PROD: `data-sharing-artifacts-${accountIdAlias.PROD}-${REGION}`
}
export const MART_S3_PREFIX = 'athena-query-results/'
export const MART_LAMBDA_FUNCTION_NAME = 'orcavault'

