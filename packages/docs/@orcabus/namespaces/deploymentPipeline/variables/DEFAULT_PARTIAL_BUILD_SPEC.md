[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [deploymentPipeline](../README.md) / DEFAULT\_PARTIAL\_BUILD\_SPEC

# Variable: DEFAULT\_PARTIAL\_BUILD\_SPEC

> `const` **DEFAULT\_PARTIAL\_BUILD\_SPEC**: `object`

Defined in: [packages/deployment-stack-pipeline/pipeline.ts:45](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/deployment-stack-pipeline/pipeline.ts#L45)

The default partial build spec for code build steps in the pipeline.

## Type Declaration

### phases

> **phases**: `object`

#### phases.install

> **install**: `object`

#### phases.install.runtime-versions

> **runtime-versions**: `object`

#### phases.install.runtime-versions.nodejs

> **nodejs**: `string` = `"22.x"`

### version

> **version**: `string` = `"0.2"`
