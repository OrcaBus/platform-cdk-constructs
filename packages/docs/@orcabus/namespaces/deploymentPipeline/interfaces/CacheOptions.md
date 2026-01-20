[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / CacheOptions

# Interface: CacheOptions

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:241](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L241)

Options for creating an S3 cache to use across build steps. If specified, a bucket will be created
for the cache under `<stackName>-CacheBucket`.

The partial buildspec must still contain definitions for paths and keys if used.

## See

https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.cache

## Extends

- `BucketCacheOptions`

## Properties

### bucket

> `readonly` **bucket**: `string`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:242](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L242)

***

### cacheNamespace?

> `readonly` `optional` **cacheNamespace**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.235.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-codebuild/lib/cache.d.ts:17

Defines the scope of the cache.
You can use this namespace to share a cache across multiple projects.

#### See

https://docs.aws.amazon.com/codebuild/latest/userguide/caching-s3.html#caching-s3-sharing

#### Default

```ts
undefined - No cache namespace, which means that the cache is not shared across multiple projects.
```

#### Inherited from

`BucketCacheOptions.cacheNamespace`

***

### prefix?

> `readonly` `optional` **prefix**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.235.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-codebuild/lib/cache.d.ts:8

The prefix to use to store the cache in the bucket

#### Inherited from

`BucketCacheOptions.prefix`
