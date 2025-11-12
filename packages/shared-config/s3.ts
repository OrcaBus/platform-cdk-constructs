import {StageName} from "./accounts";

/**
 * The default S3 bucket names used for pipeline data.
 */
export const PIPELINE_CACHE_BUCKET: Record<StageName, string> = {
  BETA: "pipeline-dev-cache-503977275616-ap-southeast-2",
  GAMMA: "pipeline-stg-cache-503977275616-ap-southeast-2",
  PROD: "pipeline-prod-cache-503977275616-ap-southeast-2",
}

/**
 * The reference data bucket
 */
export const REFERENCE_DATA_BUCKET = "reference-data-503977275616-ap-southeast-2"

/**
 * The test data bucket
 */
export const TEST_DATA_BUCKET = "test-data-503977275616-ap-southeast-2"

/**
 * The default S3 prefixes used for pipeline data.
 */
export const PIPELINE_CACHE_PREFIX: Record<StageName, string> = {
  BETA: "byob-icav2/development/",
  GAMMA: "byob-icav2/staging/",
  PROD: "byob-icav2/production/",
}

/**
 * The oncoanalyser bucket.
 */
export const ONCOANALYSER_BUCKET: Record<StageName, string> = {
  BETA: 'umccr-temp-dev',
  GAMMA: 'umccr-temp-stg',
  PROD: 'org.umccr.data.oncoanalyser',
}

/**
 * The analysis archive bucket.
 */
export const ANALYSIS_ARCHIVE_BUCKET = "archive-prod-analysis-503977275616-ap-southeast-2";

/**
 * The fastq archive bucket.
 */
export const FASTQ_ARCHIVE_BUCKET = "archive-prod-fastq-503977275616-ap-southeast-2";