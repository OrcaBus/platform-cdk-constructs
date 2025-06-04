/**
 *
 * Shared configuration should now be placed in the shared-config package.
 *
 */

import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";
import { SynthesisMessage } from "aws-cdk-lib/cx-api";

/**
 * @deprecated Import from `@orcabus/platform-cdk-constructs/shared-config/accounts` instead.
 */
export type StageName = "BETA" | "GAMMA" | "PROD";
/**
 * @deprecated Import from `@orcabus/platform-cdk-constructs/shared-config/accounts` instead.
 */
export const region = "ap-southeast-2";
/**
 * @deprecated Import from `@orcabus/platform-cdk-constructs/shared-config/accounts` instead.
 */
export const accountIdAlias: Record<StageName, string> = {
  BETA: "843407916570", // umccr_development
  GAMMA: "455634345446", // umccr_staging
  PROD: "472057503814", // umccr_production
};

export function resolveStageName(scope: Construct): StageName {
  // See discussion in https://github.com/aws/aws-cdk/issues/1754
  // Use Stack.of(scope).account to get the account ID instead of
  // cdk.Aws.ACCOUNT_ID, which may not be available at this point in the CDK lifecycle.
  const match = Object.entries(accountIdAlias).find(
    ([_, value]) => value === Stack.of(scope).account,
  );

  if (!match) {
    throw new Error(
      `Account ID ${Stack.of(scope).account} not found in accountIdAlias`,
    );
  }

  return match[0] as StageName;
}

/**
 * Stringify the message data.
 */
export function synthesisMessageToString(sm: SynthesisMessage): string {
  return `${JSON.stringify(sm.entry.data)} [${sm.id}]`;
}

/**
 * Validate the secret name so that it doesn't end with 6 characters and a hyphen.
 */
export const validateSecretName = (secretName: string) => {
  // Note, this should not end with a hyphen and 6 characters, otherwise secrets manager won't be
  // able to find the secret using a partial ARN.
  if (/-(.){6}$/.test(secretName)) {
    throw new Error(
      "the secret name should not end with a hyphen and 6 characters",
    );
  }
};

/**
 * TODO: Move to shared-config package
 */

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

export const icav2ProjectId: Record<StageName, string> = {
  BETA: "ea19a3f5-ec7c-4940-a474-c31cd91dbad4", // development
  GAMMA: "157b9e78-b2e1-45a7-bfcd-691159995f7c", // staging
  PROD: "eba5c946-1677-441d-bbce-6a11baadecbb", // production
};
