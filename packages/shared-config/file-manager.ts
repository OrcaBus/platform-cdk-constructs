/**
 * Shared config for the FileManager.
 */

import { validateSecretName } from "../utils";
import {
  BETA_ENVIRONMENT,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
} from "../deployment-stack-pipeline";
import {StageName} from "./accounts";

export const fileManagerBuckets: Record<StageName, string[]> = {
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

export const fileManagerCacheBuckets: Record<StageName, string[]> = {
  BETA: ["pipeline-dev-cache-503977275616-ap-southeast-2"],
  GAMMA: ["pipeline-stg-cache-503977275616-ap-southeast-2"],
  PROD: ["pipeline-prod-cache-503977275616-ap-southeast-2"],
};

export const fileManagerPresignUserSecret = "orcabus/file-manager-presign-user"; // pragma: allowlist secret
export const accessKeySecretArn: Record<StageName, string> = {
  BETA: `arn:aws:secretsmanager:${BETA_ENVIRONMENT.region}:${BETA_ENVIRONMENT.account}:secret:${fileManagerPresignUserSecret}`,
  GAMMA: `arn:aws:secretsmanager:${GAMMA_ENVIRONMENT.region}:${GAMMA_ENVIRONMENT.account}:secret:${fileManagerPresignUserSecret}`,
  PROD: `arn:aws:secretsmanager:${PROD_ENVIRONMENT.region}:${PROD_ENVIRONMENT.account}:secret:${fileManagerPresignUserSecret}`,
};

export const fileManagerIngestRoleName = "orcabus-file-manager-ingest-role";
validateSecretName(fileManagerPresignUserSecret);

export const fileManagerPresignUser = "orcabus-file-manager-presign-user"; // pragma: allowlist secret
export const fileManagerDomainPrefix = "file";
