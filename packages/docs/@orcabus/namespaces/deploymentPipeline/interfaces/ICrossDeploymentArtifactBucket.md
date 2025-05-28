[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / ICrossDeploymentArtifactBucket

# Interface: ICrossDeploymentArtifactBucket

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:26](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L26)

## Properties

### artifactBucket

> `readonly` **artifactBucket**: `IBucket`

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:30](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L30)

The S3 bucket used to store artifacts for cross-deployment pipelines.

***

### artifactKms

> `readonly` **artifactKms**: `IKey`

Defined in: [packages/deployment-stack-pipeline/artifact-bucket.ts:34](https://github.com/OrcaBus/platform-cdk-constructs/blob/885f4bf19a11a54aff506f0fbbcc9831b1a2976f/packages/deployment-stack-pipeline/artifact-bucket.ts#L34)

The KMS key used to encrypt artifacts for cross-deployment pipelines.
