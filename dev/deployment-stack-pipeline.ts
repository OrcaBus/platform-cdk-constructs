#!/usr/bin/env node
import "source-map-support/register";
import { Construct } from "constructs";
import * as cdk from "aws-cdk-lib";
import { DeploymentStackPipeline } from "../packages/deployment-stack-pipeline";
import { Bucket } from "aws-cdk-lib/aws-s3";

const AWS_TOOLCHAIN_ACCOUNT = "383856791668";
const AWS_TOOLCHAIN_REGION = "ap-southeast-2";

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
      removalPolicy: cdk.RemovalPolicy.DESTROY, // NOT recommended for production code
      autoDeleteObjects: true, // NOT recommended for production code
    });
  }
}

class DevStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    new DeploymentStackPipeline(this, "DeploymentPipeline", {
      githubBranch: "main",
      githubRepo: "umccr/micro-service",
      stack: DeploymentStack,
      stackName: "TestStack",
      stackConfig: {
        beta: { bucketName: "my-simple-bucket-dev" },
        gamma: { bucketName: "my-simple-bucket-stg" },
        prod: { bucketName: "my-simple-bucket-prod" },
      },
      pipelineName: "TestDeploymentPipeline",
      cdkSynthCmd: ["yarn install --immutable", "yarn cdk synth"],
    });
  }
}

new DevStack(app, "DevStack", {
  env: {
    account: AWS_TOOLCHAIN_ACCOUNT,
    region: AWS_TOOLCHAIN_REGION,
  },
  tags: {
    "umccr-org:Stack": "DevStack",
    "umccr-org:Product": "OrcaBus",
  },
});

app.synth();
