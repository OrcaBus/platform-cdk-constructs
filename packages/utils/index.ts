import * as cdk from "aws-cdk-lib";
import {Construct} from "constructs";
import {Stack} from "aws-cdk-lib";

export type StageName = "BETA" | "GAMMA" | "PROD";

export const region = 'ap-southeast-2';

export const accountIdAlias: Record<StageName, string> = {
  BETA: '843407916570', // umccr_development
  GAMMA: '455634345446', // umccr_staging
  PROD: '472057503814', // umccr_production
};

export function resolveStageName(scope: Construct): StageName {
    // See discussion in https://github.com/aws/aws-cdk/issues/1754
    // Use Stack.of(scope).account to get the account ID instead of
    // cdk.Aws.ACCOUNT_ID, which may not be available at this point in the CDK lifecycle.
    const match = Object.entries(accountIdAlias).find(([_, value]) => value === Stack.of(scope).account)

    if (!match) {
        throw new Error(`Account ID ${Stack.of(scope).account} not found in accountIdAlias`);
    }

    return match[0] as StageName;
}