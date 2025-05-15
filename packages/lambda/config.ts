import {accountIdAlias, region, StageName} from "../utils";

export const DEFAULT_ORCABUS_TOKEN_SECRET_ID =  'orcabus/token-service-jwt'
export const DEFAULT_HOSTNAME_SSM_PARAMETER = '/hosted_zone/umccr/name'

export const MART_ENV_VARS = {
    ATHENA_WORKGROUP_NAME: 'orcahouse',
    ATHENA_DATASOURCE_NAME: 'orcavault',
    ATHENA_DATABASE_NAME: 'mart'
}

export const MART_S3_BUCKET: Record<StageName, string> = {
    BETA: `data-sharing-artifacts-${accountIdAlias.BETA}-${region}`,
    GAMMA: `data-sharing-artifacts-${accountIdAlias.GAMMA}-${region}`,
    PROD: `data-sharing-artifacts-${accountIdAlias.PROD}-${region}`
}
export const MART_S3_PREFIX = 'athena-query-results/'
export const MART_LAMBDA_FUNCTION_NAME = 'orcavault'
