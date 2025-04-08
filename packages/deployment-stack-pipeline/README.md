# DeploymentStackPipeline

This construct will deploy stack defined as props across 3 stages in our Beta, Gamma, and Prod environment.

Usage example

```ts
new DeploymentStackPipeline(this, "DeploymentPipeline", {
  githubBranch: "main",
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

```
