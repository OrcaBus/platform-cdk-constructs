import * as cdk from 'aws-cdk-lib'
import {Construct} from "constructs";
import {addGitCommitIdOutput} from "../utils/index";

/**
 * Extends cdk.Stack with a CfnOutput GitCommitId
 * Allows us to see which version of a stack is currently deployed into an environment
 */
export class GitStack extends cdk.Stack {
  // Extends Stack with a GitCommitId CloudFormation output
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    addGitCommitIdOutput(this);
  }
}
