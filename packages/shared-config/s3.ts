import {StageName} from "./accounts";

export const pipelineCacheBucket: Record<StageName, string> = {
  BETA: "pipeline-dev-cache-503977275616-ap-southeast-2",
  GAMMA: "pipeline-stg-cache-503977275616-ap-southeast-2",
  PROD: "pipeline-prod-cache-503977275616-ap-southeast-2",
};
export const pipelineCachePrefix: Record<StageName, string> = {
  BETA: "byob-icav2/development/",
  GAMMA: "byob-icav2/staging/",
  PROD: "byob-icav2/production/",
};

