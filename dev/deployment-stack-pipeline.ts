#!/usr/bin/env node
import "source-map-support/register";
import { Construct } from "constructs";
import * as cdk from "aws-cdk-lib";
import {
  DeploymentStackPipeline,
  TOOLCHAIN_ENVIRONMENT,
} from "../packages/deployment-stack-pipeline";
import { Bucket } from "aws-cdk-lib/aws-s3";

const app = new cdk.App();

class DeploymentStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    props: cdk.StackProps & { bucketName: string },
  ) {
    super(scope, id, props);

    new Bucket(this, "MySimpleBucket", {
      bucketName: props.bucketName,
      versioned: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
  }
}

class DevStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    new DeploymentStackPipeline(this, "DeploymentPipeline", {
      githubBranch: "feat/add-kms-policy",
      githubRepo: "platform-cdk-constructs",
      stack: DeploymentStack,
      stackName: "TestStack",
      stackConfig: {
        beta: { bucketName: "my-simple-bucket-dev" },
        gamma: { bucketName: "my-simple-bucket-stg" },
        prod: { bucketName: "my-simple-bucket-prod" },
      },
      pipelineName: "TestDeploymentPipeline",
      cdkSynthCmd: [
        "pnpm install --frozen-lockfile --ignore-scripts",
        "cd dev",
        "pnpm cdk synth",
      ],
      cdkOut: "dev/cdk.out",
    });
  }
}

new DevStack(app, "DevStack", {
  env: TOOLCHAIN_ENVIRONMENT,
  tags: {
    "umccr-org:Stack": "DevStack",
    "umccr-org:Product": "OrcaBus",
  },
});

app.synth();
