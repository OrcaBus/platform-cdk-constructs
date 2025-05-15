import * as cdk from "aws-cdk-lib";

export type StageName = "BETA" | "GAMMA" | "PROD";

export const region = 'ap-southeast-2';

export const accountIdAlias: Record<StageName, string> = {
  BETA: '843407916570', // umccr_development
  GAMMA: '455634345446', // umccr_staging
  PROD: '472057503814', // umccr_production
};

export function resolveStageName(): StageName {
    const match = Object.entries(accountIdAlias).find(([_, value]) => value === cdk.Aws.ACCOUNT_ID)

    if (!match) {
        throw new Error(`Account ID ${cdk.Aws.ACCOUNT_ID} not found in accountIdAlias`);
    }

    return match[0] as StageName;
}