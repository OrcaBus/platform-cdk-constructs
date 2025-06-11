import {StageName} from "./accounts";

/**
 * @deprecated Use PIPELINE_CACHE_BUCKET instead
 */
export const pipelineCacheBucket: Record<StageName, string> = {
  BETA: "pipeline-dev-cache-503977275616-ap-southeast-2",
  GAMMA: "pipeline-stg-cache-503977275616-ap-southeast-2",
  PROD: "pipeline-prod-cache-503977275616-ap-southeast-2",
};

/**
 * The default S3 bucket names used for pipeline data.
 */
export const PIPELINE_CACHE_BUCKET: Record<StageName, string> = {
  BETA: "pipeline-dev-cache-503977275616-ap-southeast-2",
  GAMMA: "pipeline-stg-cache-503977275616-ap-southeast-2",
  PROD: "pipeline-prod-cache-503977275616-ap-southeast-2",
}

/**
 * @deprecated Use PIPELINE_CACHE_PREFIX instead
 */
export const pipelineCachePrefix: Record<StageName, string> = {
  BETA: "byob-icav2/development/",
  GAMMA: "byob-icav2/staging/",
  PROD: "byob-icav2/production/",
};

/**
 * The default S3 prefixes used for pipeline data.
 */
export const PIPELINE_CACHE_PREFIX: Record<StageName, string> = {
  BETA: "byob-icav2/development/",
  GAMMA: "byob-icav2/staging/",
  PROD: "byob-icav2/production/",
}

