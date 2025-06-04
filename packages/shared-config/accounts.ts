/**
 * Supported deployment stage names.
 */
export type StageName = "BETA" | "GAMMA" | "PROD";

/**
 * Default AWS region for all environments.
 */
export const REGION = "ap-southeast-2";

/**
 * Beta Account ID.
 */
export const BETA_ACCOUNT_ID = "843407916570";
/**
 * Gamma Account ID.
 */
export const GAMMA_ACCOUNT_ID = "455634345446";
/**
 * Production Account ID.
 */
export const PROD_ACCOUNT_ID = "472057503814";

/**
 * Mapping from stage name to AWS Account ID.
 */
export const accountIdAlias: Record<StageName, string> = {
  BETA: BETA_ACCOUNT_ID,
  GAMMA: GAMMA_ACCOUNT_ID,
  PROD: PROD_ACCOUNT_ID,
};
