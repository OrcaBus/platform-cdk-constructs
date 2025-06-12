/**
 *
 * Shared configuration should now be placed in the shared-config package.
 *
 */

import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";
import { SynthesisMessage } from "aws-cdk-lib/cx-api";
import { accountIdAlias, StageName } from "../shared-config/accounts";

export function resolveStageName(scope: Construct): StageName {
  // See discussion in https://github.com/aws/aws-cdk/issues/1754
  // Use Stack.of(scope).account to get the account ID instead of
  // cdk.Aws.ACCOUNT_ID, which may not be available at this point in the CDK lifecycle.
  const match = Object.entries(accountIdAlias).find(
    ([_, value]) => value === Stack.of(scope).account,
  );

  if (!match) {
    // Check if 'stageName' is a property in the variable 'scope'
    // This is useful for cases where the account ID is not found in accountIdAlias
    // but the stage name is provided as a construct attribute.
    const stackObj = scope.node.scope;
    const propertyNames = Object.getOwnPropertyNames(stackObj);
    if (!propertyNames.includes("stageName")) {
      throw new Error(
        `Account ID ${Stack.of(scope).account} not found in accountIdAlias.
        Please set 'stageName' as a construct attribute in your stack as a fallback`,
      );
    }
    // If 'stageName' is present, return it as a StageName
    return Object(stackObj)["stageName"] as StageName;
  }

  return match[0] as StageName;
}

/**
 * Stringify the message data.
 */
export function synthesisMessageToString(sm: SynthesisMessage): string {
  return `${JSON.stringify(sm.entry.data)} [${sm.id}]`;
}
