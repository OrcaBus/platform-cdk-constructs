/**
 * Shared config for the FileManager.
 */

import {
  BETA_ENVIRONMENT,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
} from "../deployment-stack-pipeline";
import { StageName } from "./accounts";
import { pipelineCacheBucket } from "./s3";
import { validateSecretName } from "./secrets";

export const FILE_MANAGER_BUCKETS: Record<StageName, string[]> = {
  BETA: [
    "umccr-temp-dev",
    `ntsm-fingerprints-${BETA_ENVIRONMENT.account}-ap-southeast-2`,
    `data-sharing-artifacts-${BETA_ENVIRONMENT.account}-ap-southeast-2`,
    "filemanager-inventory-test",
  ],
  GAMMA: [
    "umccr-temp-stg",
    `ntsm-fingerprints-${GAMMA_ENVIRONMENT.account}-ap-southeast-2`,
    `data-sharing-artifacts-${GAMMA_ENVIRONMENT.account}-ap-southeast-2`,
  ],
  PROD: [
    "org.umccr.data.oncoanalyser",
    "archive-prod-analysis-503977275616-ap-southeast-2",
    "archive-prod-fastq-503977275616-ap-southeast-2",
    `ntsm-fingerprints-${PROD_ENVIRONMENT.account}-ap-southeast-2`,
    `data-sharing-artifacts-${PROD_ENVIRONMENT.account}-ap-southeast-2`,
    "pipeline-montauk-977251586657-ap-southeast-2",
  ],
};

export const FILE_MANAGER_CACHE_BUCKETS: Record<StageName, string[]> = {
  BETA: [pipelineCacheBucket.BETA],
  GAMMA: [pipelineCacheBucket.GAMMA],
  PROD: [pipelineCacheBucket.PROD],
};

export const FILE_MANAGER_PRESIGN_USER_SECRET =
  "orcabus/file-manager-presign-user"; // pragma: allowlist secret
validateSecretName(FILE_MANAGER_PRESIGN_USER_SECRET);

export const FILE_MANAGER_ACCESS_KEY_ARNS: Record<StageName, string> = {
  BETA: `arn:aws:secretsmanager:${BETA_ENVIRONMENT.region}:${BETA_ENVIRONMENT.account}:secret:${FILE_MANAGER_PRESIGN_USER_SECRET}`,
  GAMMA: `arn:aws:secretsmanager:${GAMMA_ENVIRONMENT.region}:${GAMMA_ENVIRONMENT.account}:secret:${FILE_MANAGER_PRESIGN_USER_SECRET}`,
  PROD: `arn:aws:secretsmanager:${PROD_ENVIRONMENT.region}:${PROD_ENVIRONMENT.account}:secret:${FILE_MANAGER_PRESIGN_USER_SECRET}`,
};

export const FILE_MANAGER_INGEST_ROLE = "orcabus-file-manager-ingest-role";
export const FILE_MANAGER_PRESIGN_USER = "orcabus-file-manager-presign-user"; // pragma: allowlist secret
export const FILE_MANAGER_DOMAIN_PREFIX = "file";
