[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CacheOptions

# Interface: CacheOptions

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:267](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L267)

Options for creating an S3 cache to use across build steps. If specified, the bucket under
`CODEBUILD_CACHE_BUCKET` will be used for caching. This bucket is managed by the shared-resources
service.

## Properties

### namespace

> `readonly` **namespace**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:272](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L272)

Specify the namespace for the cache. This option is required because the cache bucket is shared across
all projects so a namespace is required to uniquely identify the cache. Use the project name, e.g. `filemanager`.

***

### paths?

> `readonly` `optional` **paths**: `string`[]

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:284](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L284)

The paths to cache. This will default to the `node_modules` directory if unspecified.

Note that if the cache is specified in the buildspec, that config will take precedence. This option is only used
as a convenience to specify paths, and will not override the buildspec cache config.

#### See

https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.cache

***

### prefix?

> `readonly` `optional` **prefix**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:276](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L276)

The prefix for the cache controlling the prefix on S3. If left unspecified, this will default to the namespace.
