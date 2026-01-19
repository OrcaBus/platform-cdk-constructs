/**
 * Shared config for the FileManager.
 */

import {
  BETA_ENVIRONMENT,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
} from "../deployment-stack-pipeline";
import { StageName } from "./accounts";
import {ANALYSIS_ARCHIVE_BUCKET, FASTQ_ARCHIVE_BUCKET, ONCOANALYSER_BUCKET, PIPELINE_CACHE_BUCKET} from "./s3";
import { validateSecretName } from "./secrets";

// The inventory bucket used for testing filemanager.
export const FILE_MANAGER_INVENTORY_BUCKET = "filemanager-inventory-test";

// Regular buckets where all data is available and ingested.
export const FILE_MANAGER_BUCKETS: Record<StageName, string[]> = {
  BETA: [
    ONCOANALYSER_BUCKET.BETA,
    FILE_MANAGER_INVENTORY_BUCKET,
    `ntsm-fingerprints-${BETA_ENVIRONMENT.account}-${BETA_ENVIRONMENT.region}`,
    `fastq-manager-sequali-outputs-${BETA_ENVIRONMENT.account}-${BETA_ENVIRONMENT.region}`,
    `data-sharing-artifacts-${BETA_ENVIRONMENT.account}-${BETA_ENVIRONMENT.region}`,
  ],
  GAMMA: [
    ONCOANALYSER_BUCKET.GAMMA,
    `ntsm-fingerprints-${GAMMA_ENVIRONMENT.account}-${GAMMA_ENVIRONMENT.region}`,
    `fastq-manager-sequali-outputs-${GAMMA_ENVIRONMENT.account}-${GAMMA_ENVIRONMENT.region}`,
    `data-sharing-artifacts-${GAMMA_ENVIRONMENT.account}-${GAMMA_ENVIRONMENT.region}`,
  ],
  PROD: [
    ONCOANALYSER_BUCKET.PROD,
    ANALYSIS_ARCHIVE_BUCKET,
    FASTQ_ARCHIVE_BUCKET,
    `ntsm-fingerprints-${PROD_ENVIRONMENT.account}-${PROD_ENVIRONMENT.region}`,
    `fastq-manager-sequali-outputs-${PROD_ENVIRONMENT.account}-${PROD_ENVIRONMENT.region}`,
    `data-sharing-artifacts-${PROD_ENVIRONMENT.account}-${PROD_ENVIRONMENT.region}`,
    `pipeline-montauk-977251586657-${PROD_ENVIRONMENT.region}`,
    "research-data-550435500918-ap-southeast-2",
    "project-data-889522050439-ap-southeast-2",
    "project-data-491085415398-ap-southeast-2",
    "project-data-071784445872-ap-southeast-2",
    "project-data-980504796380-ap-southeast-2"
  ],
};

// Cache buckets where the `byob-icav2/*/cache/*` pattern is ignored for the ingester.
export const FILE_MANAGER_CACHE_BUCKETS: Record<StageName, string[]> = {
  BETA: [PIPELINE_CACHE_BUCKET.BETA],
  GAMMA: [PIPELINE_CACHE_BUCKET.GAMMA],
  PROD: [PIPELINE_CACHE_BUCKET.PROD],
};

// Cross account buckets where the dev/stg/prod filemanager instances should all ingest the same bucket,
// so more care needs to be taken when tagging objects.
export const FILE_MANAGER_CROSS_ACCOUNT_BUCKETS: string[] = [
    "test-data-503977275616-ap-southeast-2"
];

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
