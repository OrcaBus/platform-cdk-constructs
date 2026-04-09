/**
 *
 * Shared configuration should now be placed in the shared-config package.
 *
 */

import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";
import * as cdk from "aws-cdk-lib";
import { SynthesisMessage } from "aws-cdk-lib/cx-api";
import {ACCOUNT_ID_ALIAS, StageName} from "../shared-config/accounts";
import {execSync} from "child_process";

export function resolveStageName(scope: Construct): StageName {
  // See discussion in https://github.com/aws/aws-cdk/issues/1754
  // Use Stack.of(scope).account to get the account ID instead of
  // cdk.Aws.ACCOUNT_ID, which may not be available at this point in the CDK lifecycle.
  const match = Object.entries(ACCOUNT_ID_ALIAS).find(
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

/**
 * Add GitCommitId tag to stack
 */

function runCommand(command: string): string | undefined {
  /**
   * Run a command and return the stdout as a string. If the command fails, return undefined.
   */
  try {
    return execSync(command, {
      encoding: 'utf-8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
  } catch {
    return undefined;
  }
}

function isShortSha(value: string): boolean {
  /**
   * Check if the value is a valid short Git SHA (7 hexadecimal characters).
   */
  return /^[0-9a-f]{7}$/i.test(value);
}

function resolveGitCommitId(): string {
  /**
   * Resolve the Git commit ID for traceability. In CodeBuild, use the resolved source version.
   * For local synths, attempt to get the current Git commit SHA.
   * If there are uncommitted changes, append '-dirty' to the SHA.
   * If the Git commit ID cannot be determined, return 'unknown'.
   */
  const codebuildSha = process.env.CODEBUILD_RESOLVED_SOURCE_VERSION?.trim();
  if (codebuildSha) {
    const shortSha = codebuildSha.substring(0, 7);
    if (isShortSha(shortSha)) {
      return shortSha;
    }
  }

  // For local synths, attempt to get the current Git commit SHA.
  const localSha = runCommand('git rev-parse --short HEAD');
  if (!localSha || !isShortSha(localSha)) {
    return 'unknown';
  }

  // Preserve traceability for local synths with uncommitted changes.
  const isDirty = Boolean(runCommand('git status --porcelain'));
  return isDirty ? `${localSha}-dirty` : localSha;
}

export function addGitCommitIdOutput(scope: Construct) {
  /**
   *  Add the git commit id as an output to the stack for traceability.
   *  (not propagated to child resources).
   */
  // Output the git commit id for traceability
  new cdk.CfnOutput(scope, 'CfnOutputGitCommitId', {
    key: "GitCommitId",
    value: resolveGitCommitId(),
    description: 'The git commit id of the deployed code',
  });
}