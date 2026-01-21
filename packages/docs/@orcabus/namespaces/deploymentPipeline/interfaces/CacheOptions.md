[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CacheOptions

# Interface: CacheOptions

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:246](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L246)

Options for creating an S3 cache to use across build steps. If specified, the bucket under
`CODEBUILD_CACHE_BUCKET` will be used for caching. This bucket is managed by the shared-resources
service.

The partial buildspec must still contain definitions for paths and keys if used.

## See

https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.cache

## Properties

### namespace

> `readonly` **namespace**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:251](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L251)

Specify the namespace for the cache. This option is required because the cache bucket is shared across
all projects so a namespace is required to uniquely identify the cache. Use the project name, e.g. `filemanager`.
