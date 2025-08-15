import {StageName} from "./accounts";

/**
 * @deprecated Use ICAV2_PROJECT_ID instead.
 */
export const icav2ProjectId: Record<StageName, string> = {
  BETA: "ea19a3f5-ec7c-4940-a474-c31cd91dbad4", // development
  GAMMA: "157b9e78-b2e1-45a7-bfcd-691159995f7c", // staging
  PROD: "eba5c946-1677-441d-bbce-6a11baadecbb", // production
};

/**
 * The default project ID for our ICA tenant
 */
export const ICAV2_PROJECT_ID: Record<StageName, string> = {
  BETA: "ea19a3f5-ec7c-4940-a474-c31cd91dbad4", // development
  GAMMA: "157b9e78-b2e1-45a7-bfcd-691159995f7c", // staging
  PROD: "eba5c946-1677-441d-bbce-6a11baadecbb", // production
}

/**
 * @deprecated Use ICAV2_ACCESS_TOKEN_SECRET_ID instead.
 */
export const icav2AccessTokenSecretId: Record<StageName, string> = {
  BETA: 'ICAv2JWTKey-umccr-prod-service-dev', // pragma: allowlist secret
  GAMMA: 'ICAv2JWTKey-umccr-prod-service-staging', // pragma: allowlist secret
  PROD: 'ICAv2JWTKey-umccr-prod-service-production', // pragma: allowlist secret
};

/**
 * The secret ID for the access token used to authenticate with the ICA API.
 */
export const ICAV2_ACCESS_TOKEN_SECRET_ID: Record<StageName, string> = {
  BETA: 'ICAv2JWTKey-umccr-prod-service-dev',  // pragma: allowlist secret
  GAMMA: 'ICAv2JWTKey-umccr-prod-service-staging',  // pragma: allowlist secret
  PROD: 'ICAv2JWTKey-umccr-prod-service-production',  // pragma: allowlist secret
}

export const ICAV2_STORAGE_CONFIGURATION_SSM_PARAMETER_PATH_PREFIX = '/icav2/umccr-prod/storage-configurations/'
export const ICAV2_PROJECT_TO_STORAGE_CONFIGURATIONS_SSM_PARAMETER_PATH_PREFIX = '/icav2/umccr-prod/project-to-storage-configurations/'
export const ICAV2_STORAGE_CREDENTIALS_SSM_PARAMETER_PATH_PREFIX = '/icav2/umccr-prod/storage-credentials/'

/**
 * @deprecated Use ICAV2_BASE_URL instead.
 */
export const icav2BaseUrl: string = "https://ica.illumina.com/ica/rest"

/**
 * The base URL for the ICA API v2.
 */
export const ICAV2_BASE_URL: string = "https://ica.illumina.com/ica/rest";