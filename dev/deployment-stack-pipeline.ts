#!/usr/bin/env node
import "source-map-support/register";
import { Construct } from "constructs";
import * as cdk from "aws-cdk-lib";
import {
  BETA_ENVIRONMENT,
  DeploymentStackPipeline,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
  TOOLCHAIN_ENVIRONMENT,
} from "../packages/deployment-stack-pipeline";
import { Bucket, BucketEncryption } from "aws-cdk-lib/aws-s3";
import { Key } from "aws-cdk-lib/aws-kms";
import * as iam from "aws-cdk-lib/aws-iam";

const app = new cdk.App();

class DeploymentStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    props: cdk.StackProps & { bucketName: string },
  ) {
    super(scope, id, props);

    new Bucket(this, "MySimpleBucket", {
      versioned: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // const myKmsKey = new Key(this, "TestArtifactBucketKmsKey", {
    //   pendingWindow: cdk.Duration.days(7),
    //   description: "Test Artifact Bucket KMS Key",
    //   enableKeyRotation: false,
    //   removalPolicy: cdk.RemovalPolicy.DESTROY,
    //   alias: `${props.bucketName}-kms-key`,
    // });
    // const artifactBucket = new Bucket(this, "TestArtifactBucket", {
    //   bucketName: props.bucketName,
    //   versioned: false,
    //   removalPolicy: cdk.RemovalPolicy.DESTROY,
    //   autoDeleteObjects: true,
    //   encryption: BucketEncryption.KMS,
    //   encryptionKey: myKmsKey,
    // });

    // artifactBucket.addToResourcePolicy(
    //   new iam.PolicyStatement({
    //     actions: ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
    //     resources: [
    //       artifactBucket.bucketArn,
    //       artifactBucket.arnForObjects("*"),
    //     ],
    //     principals: [
    //       new iam.ArnPrincipal(
    //         `arn:aws:iam::${BETA_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${BETA_ENVIRONMENT.account}-ap-southeast-2`,
    //       ),
    //       new iam.ArnPrincipal(
    //         `arn:aws:iam::${GAMMA_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${GAMMA_ENVIRONMENT.account}-ap-southeast-2`,
    //       ),
    //       new iam.ArnPrincipal(
    //         `arn:aws:iam::${PROD_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${PROD_ENVIRONMENT.account}-ap-southeast-2`,
    //       ),
    //     ],
    //   }),
    // );
  }
}

class DevStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    new DeploymentStackPipeline(this, "DeploymentPipeline", {
      githubBranch: "feat(cdk-pipeline)/unify-kms-key",
      githubRepo: "platform-cdk-constructs",
      stack: DeploymentStack,
      stackName: "TestStack",
      stackConfig: {
        beta: { bucketName: "my-simple-bucket-dev" },
        gamma: { bucketName: "my-simple-bucket-stg" },
        prod: { bucketName: "my-simple-bucket-prod" },
      },
      pipelineName: "TestNumber2DeploymentPipeline",
      cdkSynthCmd: [
        "pnpm install --frozen-lockfile --ignore-scripts",
        "cd dev",
        "pnpm cdk synth",
      ],
      cdkOut: "dev/cdk.out",
    });
  }
}

// new DevStack(app, "DevStack", {
//   env: TOOLCHAIN_ENVIRONMENT,
//   tags: {
//     stack: "manual",
//     useCase: "testing",
//   },
// });

new DevStack(app, "DevSecondStack", {
  env: TOOLCHAIN_ENVIRONMENT,
  tags: {
    stack: "manual",
    useCase: "testing",
  },
});

// new DeploymentStack(app, "ArtifactBucketTestStack", {
//   env: TOOLCHAIN_ENVIRONMENT,
//   tags: {
//     stack: "manual",
//     useCase: "testing",
//   },
//   bucketName: "test-artifact-bucket-william",
// });

app.synth();
