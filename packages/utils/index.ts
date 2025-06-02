import * as cdk from "aws-cdk-lib";
import {Construct} from "constructs";
import {Stack} from "aws-cdk-lib";
import { SynthesisMessage } from 'aws-cdk-lib/cx-api';

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
        throw new Error('the secret name should not end with a hyphen and 6 characters');
    }
};
